# Minor documentation errors at `:h vim9`

Whenever you  add an item  here, update the documentation  in your Vim  fork, in
the  `fix-vim9-doc` branch.   Then,  redirect  the output  of  `$  git diff`  in
`~/Desktop/patch.txt`.  Suggest the final patch in a report.

## 134

> In all cases the function must be defined before used.  That is when it is
> first called or when `:defcompile` causes **the call** to be compiled.

Should be "the function".

## 141

> Global functions can be still be defined and deleted at nearly any time.  In
> Vim9 script script-local functions are defined once when the script is sourced
> and cannot be deleted or replaced.

Maybe add a comma  after "In Vim9 script", to avoid  having script written twice
consecutively.

## 167

From `:h vim9-declaration /echo inner  " Error!`:

    echo inner  " Error!

You can't use `"` as an inline  comment leader after `:echo`, because the latter
parses `"`  as the  start of  a string.  Instead,  the doc  should write  one of
these:

    echo inner  # Error!
    echo inner  |" Error!

More generally, there are a lot of inline comments at `:h vim9` using `"` as the
comment leader:

    167
    echo inner  " Error!

    184
    echo temp  " Error!

    212-220
    myList->add(123)		" works
    g:myList->add(123)		" works
    [1, 2, 3]->Process()		" works
    #{a: 1, b: 2}->Process()	" works
    {'a': 1, 'b': 2}->Process()	" works
    "foobar"->Process()		" does NOT work
    ("foobar")->Process()		" works
    'foobar'->Process()		" does NOT work
    ('foobar')->Process()		" works

    351-353
    let var=234	" Error!
    let var= 234	" Error!
    let var =234	" Error!

    355
    let var = 234	" OK

    365-373
    call Func (arg)	   " Error!
    call Func
         \ (arg)	   " Error!
    call Func(arg)	   " OK
    call Func(
         \ arg)	   " OK
    call Func(
         \ arg	   " OK
         \ )

    425-434
    ->		" legacy Vim: shifts the previous line to the right
    ->func()	" Vim9: method call
    :->		" Vim9: shifts the previous line to the right

    %s/a/b          " legacy Vim: substitute on all lines
    x = alongname
         % another  " Vim9: line continuation without a backslash
    :%s/a/b         " Vim9: substitute on all lines
    'text'->func()  " Vim9: method call
    :'t             " legacy Vim: jump to mark m

    449
    use-feature  " May give compilation error

    620-621
    let var = 0		" infers number type
    let var = 'hello'	" infers string type

    832
    const greeting = 'hello'  " string type is inferred

    842
    return result || 0	" returns 1

    847
    return result || 0	" returns 44

I think they're  all wrong, because only  `#` works as an  inline comment leader
inside a `:def` function (since 8.2.1125?).

## 191

> Variables may shadow Ex commands, rename the variable if needed.
                                ^
                                ✘

Should be a semicolon; better than a comma splice.
<https://en.wikipedia.org/wiki/Comma_splice>

## 231

> This is required to be able have cyclic dependencies between functions.

I think it should be:

> This is required to be able to have cyclic dependencies between functions.
                            ^^

## 268

> For **binary** operators in expressions not in [], {} or () a line break is
> possible just before or after the operator.  For example: >
> 	let text = lead
> 		   .. middle
> 		   .. end
> 	let total = start +
> 	            end -
> 		    correction
> 	let result = positive
> 			**?** PosFunc(arg)
> 			**:** NegFunc(arg)

`?:` is not a binary operator; it's a ternary one.
So, this would be better:

> For **binary and ternary** operators ...

## 294

> This will assign "start" and print a line: >
                                   ^
                                   ✘

And print "the next" line.

## 451

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

There is a typo:

>            call MaybyInner()
                    ^
                    ✘

I think it should be:

           call MaybeInner()
                    ^
                    ✔

## 470

From `:h :def`:

    :def[!] {name}([arguments])[: {return-type}

I think a closing bracket is missing:

    :def[!] {name}([arguments])[: {return-type}]
                                               ^

## 496

> [!] is used as with `:function`.  Note that in Vim9
> script**,** script-local functions cannot be deleted or
> redefined later in the same script.

The comma  makes the second sentence  a little more readable;  no awkward double
"script".

## 566

                                                                      v
> There is no array type, use list<{type}> instead.  For a list constant**,** an
> efficient implementation is used that avoids allocating lot of small pieces of
> memory.

Add a comma to improve the readability.

## 570

> A partial and function can be declared in more or less specific ways:
> func                            any kind of function reference**;** no type
>                                 checking for arguments or return value
> func: {type}                    any number and type of arguments with specific
>                                 return type
> func({type})                    function with argument type**;** does not return
>                                 a value
> func({type}): {type}            function with argument type and return type
> func(?{type})                   function with type of optional argument**;** does
>                                 not return a value
> func(...{type})                 function with type of variable number of
>                                 arguments**;** does not return a value
> func({type}, ?{type}, ...{type}): {type}
>                                 function with:
>                                 - type of mandatory argument
>                                 - type of optional argument
>                                 - type of variable number of arguments
>                                 - return type

Notice how we've replaced the commas with semicolons.
I *think* it's more correct.
>
> If the return type is "void"**,** the function does not return a value.
                            ^

More readable.

## 592

> The reference can also be a |Partial|, in which case it stores extra arguments
> and/or a dictionary, which are not visible to the caller.  Since they are
> called in the same way**,** the declaration is the same.
                      ^

## 638

                                            v
>     To recognize a file that can be imported**,** the `vim9script` statement must
>     appear as the first statement in the file.

## 666

>     export let someValue = ...

`someValue` is a poorly chosen name.  It evokes a value, while it should evoke a
variable.  This would be better:

>     export let someVariable = ...

Note that `someValue` is used on other lines.

Line 675:

>     export {EXPORTED_CONST, someValue, MyFunc, MyClass}
                            ^-------^

Line 688:

>     import {someValue, MyClass} from "thatscript.vim"
            ^-------^

Line 692:

>     import {someValue, MyClass as ThatClass} from "myclass.vim"
            ^-------^

Line 697:

                                                  v-------v
>     Then you can use "That.EXPORTED_CONST", "That.someValue", etc.  You are free
>     to choose the name "That", but it is highly recommended to use the name of the
>     script file to avoid confusion.

## 702

> - A relative path, starting **with** "." or "..".  This finds a file relative to the

## 731

>     2. In the autocommand script do the actual work.  You can import items from
              ^---------^
              ✘
              it should be "autoload"

## 782

>     When compiling lines of Vim commands into instructions as much as possible
>     should be done at compile time.

Maybe it's just me, but I find the sentence easier to understand with a comma:

                                                          v
>     When compiling lines of Vim commands into instructions, as much as possible
>     should be done at compile time.

## 789

>     The error can be given at compile time**;** no error handling is needed at runtime.
                                          ^

## 876

> When sourcing a Vim9 script from a legacy script, only the items defined
> globally can be used, not the exported items.

Actually, I think you can also use any item defined in the `b:`, `t:`, and `w:` namespace;
but not one defined in the `s:` namespace.

##
# provide a "sid()" function to manually translate the "s:" function scope or the pseudo-key "<SID>"

**Is your feature request about something that is currently impossible or hard to do? Please describe the problem.**

It is not easy to manually translate the `s:` function scope or the pseudo-key `<SID>`.

That's an issue – for example – when one need to assign a script-local function name to an option; this doesn't work:
```vim
let &l:includeexpr = 's:my_includeexpr()'
```
When pressing `gf` on a path which can't be found, `E120` is raised:

    E120: Using <SID> not in a script context: s:my_includeexpr

**Describe the solution you'd like**

A `sid()` function which translates the `s:` function scope and the `<SID>` pseudo-key into the string `<SNR>123_`, where `123`is the id of the current script.  With it, one could write:
```vim
let &l:includeexpr = sid() .. 'my_includeexpr()'
```
**Describe alternatives you've considered**

The current general workaround is to emulate `sid()` with a custom function:
```vim
if !exists('s:SID')
    fu s:SID() abort
        return expand('<sfile>')->matchstr('<SNR>\zs\d\+\ze_SID$')->str2nr()
    endfu
    const s:SID = s:SID()->printf('<SNR>%d_')
    delfu s:SID
endif

let &l:includeexpr = s:SID .. 'my_includeexpr()'
```
It works, but it makes the code more verbose.  It would be easier to read/write if we had a builtin `sid()` function.

As an example, that's what [`vim-matchup`](https://github.com/andymass/vim-matchup/blob/24c17f94e0db86b155f1b775c3204a6829be5ee9/autoload/matchup.vim#L290-L293) does:
```vim
function! s:snr()
  return str2nr(matchstr(expand('<sfile>'), '<SNR>\zs\d\+\ze_snr$'))
endfunction
let s:sid = printf("\<SNR>%d_", s:snr())
```
and [`vim-Verdin`](https://github.com/machakann/vim-Verdin/blob/7ff7c1a42f5c60848dacda9f2c03347bd0a81500/autoload/Verdin/Completer.vim#L4-L8):
```vim
function! s:SID() abort
  return matchstr(expand('<sfile>'), '<SNR>\zs\d\+\ze_SID$')
endfunction
let s:SID = printf("\<SNR>%s_", s:SID())
delfunction s:SID
```
and [`vim-sandwich`](https://github.com/machakann/vim-sandwich/blob/02e3b6d1ff9ce346c115166855137b318b63c536/autoload/sandwich/highlight.vim#L24-L28):
```vim
function! s:SID() abort
  return matchstr(expand('<sfile>'), '<SNR>\zs\d\+\ze_SID$')
endfunction
let s:SID = printf("\<SNR>%s_", s:SID())
delfunction s:SID
```
---

Sometimes, we can also use `function()`:
```vim
let &l:includeexpr = function('s:my_includeexpr')->string() .. '()'
```
But it looks awkward, and a builtin `sid()` would still make the code easier to read/write.

Besides, you have to make sure that `s:my_includeexpr()` is defined *before* setting `'includeexpr'`. Similarly, with `s:SID()`, you have to make sure that the function is defined before you invoke it.

With `sid()`, there would be no such requirement.

Also, note that `function()` does not always work.  For example, it doesn't for `'operatorfunc'`:

    vim -Nu NONE -S <(cat <<'EOF'
        nno <expr> <c-b> <sid>setup()
        fu s:setup()
            let &opfunc = function('s:op')->string()
            return 'g@'
        endfu
        fu s:op(type)
            echom a:type
        endfu
    EOF
    )

    " press:  C-b l

    E117: Unknown function: function('<SNR>1_op')

Nor for `'completefunc'`:

    vim -Nu NONE -S <(cat <<'EOF'
        let s:matches = ['foo', 'bar', 'baz']
        fu s:complete_words(findstart, base) abort
            if a:findstart
                return searchpos('\<', 'bnW', line('.'))[1] - 1
            else
                return filter(copy(s:matches), {_,v -> stridx(v, a:base) == 0})
            endif
        endfu
        let &l:cfu = function('s:complete_words')->string()
    EOF
    )

    " press:  i C-x C-u

    E117: Unknown function: function('<SNR>1_complete_words')

And more generally, it probably doesn't work for any option which expects a function name, instead of an expression.

 - 'completefunc'
 - 'imactivatefunc'
 - 'imstatusfunc'
 - 'omnifunc'
 - 'operatorfunc'
 - 'quickfixtextfunc'
 - 'tagfunc'

**Additional context**

It's not an issue just when setting an option.  It's also an issue when starting a timer:

    vim -Nu NONE -S <(cat <<'EOF'
        call timer_start(0, 's:func')
        fu s:func(_) abort
            echom 'test'
        endfu
    EOF
    )

    E120: Using <SID> not in a script context: s:func

And when you need to invoke a script-local function from a command-line populated by a script:

    vim -Nu NONE -S <(cat <<'EOF'
        noremap <expr><silent> <c-b> Func()
        fu Func()
            let mode = mode(1)
            if mode is# "\<c-v>"
                let mode = "\<c-v>\<c-v>"
            endif
            return string(mode)->printf(":\<c-u>call s:func(%s)\<cr>")
        endfu
        fu s:func(mode)
            echom 'the mapping was pressed while in ' .. a:mode .. ' mode'
        endfu
    EOF
    )

    " press:  C-b

    E81: Using <SID> not in a script context

---

If such a function was provided, I think it should accept an optional argument to additionally make Vim translate the pseudo key `<SNR>` into a byte sequence (e.g. `<80><fd>R`).  Most of the time, it's either not needed (e.g. in a timer's callback, or in an option setting), or not desirable (e.g. when invoking a script-local function from a command-line populated by a script).  But sometimes, it *is* needed.  See [here](https://github.com/machakann/vim-Verdin/blob/7ff7c1a42f5c60848dacda9f2c03347bd0a81500/autoload/Verdin/Completer.vim#L711) and [there](https://github.com/machakann/vim-Verdin/blob/7ff7c1a42f5c60848dacda9f2c03347bd0a81500/autoload/Verdin/Verdin.vim#L289) for 2 examples.

---

Update: In the future, we may not need `sid()` to set options:
<https://github.com/vim/vim/pull/6499#issuecomment-661119363>

We may be able to use lambdas, funcrefs and partials.
Incidentally, this  should also allow us  to pass arbitrary data  to `'opfunc'`,
which is  awkward/cumbersome right now (you  need to use global  or script-local
variables...).

---

Update: If you post a report, mention that  you also need to expand `s:` for the
third optional argument of `input()`.
```vim
if !exists('s:SID')
    fu s:SID() abort
        return expand('<sfile>')->matchstr('<SNR>\zs\d\+\ze_SID$')->str2nr()
    endfu
    const s:SID = s:SID()->printf('<SNR>%d_')
    delfu s:SID
endif

fu s:CompleteWords(_a, _l, _p) abort
    return getline(1, '$')->join(' ')->split('\s\+')
        \ ->filter('v:val =~# "^\\a\\k\\+$"')
        \ ->sort()->uniq()->join("\n")
endfu

let word = input('word: ', '', 'custom,'..s:SID..'CompleteWords')
```

##
# Vim9: `:def` can't be followed by "!"

**Describe the bug**

`:def` can't be followed by `!`.

**To Reproduce**

Run this shell command:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def! Func()
        enddef
    EOF
    )

`E477` and `E193` are raised:

    Error detected while processing ...
    line    2:
    E477: No ! allowed
    line    3:
    E193: :enddef not inside a function

**Expected behavior**

No error is raised.

**Environment**

 - Vim version: 8.2 Included patches: 1-1253
 - OS: Ubuntu 16.04.6 LTS
 - Terminal: XTerm(356)

**Additional context**

According to `:h :def`, `:def` can be followed by `!`:

> [!] is used as with `:function`.  Note that in Vim9
> script script-local functions cannot be deleted or
> redefined later in the same script.

# Vim9: name of `:def` function can't start with a lowercase alphabetic character

Since a `:def` function is script-local  by default, and a script-local `:fu` or
`:def`  function *can*  start with  a  lowercase alphabetic  character, I  would
expect  being able  to start  the name  of a  `:def` function  with a  lowercase
alphabetic character.

# Vim9: can't nest a global ":def" function

**Describe the bug**

We can't nest a global `:def` function inside another `:def` function.

**To Reproduce**

Run this shell command:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Foo()
            def g:Bar()
            enddef
        enddef
        defcompile
    EOF
    )

`E124` is raised:

    Error detected while processing function <SNR>1_Foo:
    line    1:
    E124: Missing '(': :Bar()

**Expected behavior**

No error is raised.

**Environment**

 - Vim version: 8.2 Included patches: 1-1253
 - OS: Ubuntu 16.04.6 LTS
 - Terminal: XTerm(356)

**Additional context**

According to `:h vim9-scopes` and `:h :def`, it's possible to nest `:def` inside another `:def`:

> When using `:function` or `:def` to specify a new function inside a function,
> the function is local to the function.  It is not possible to define a
> script-local function inside a function. It is possible to define a global
> function, using the "g:" prefix.

> NOTE: It is possible to nest `:def` inside another
> `:def`, but it is not possible to nest `:def` inside
> `:function`, for backwards compatibility.

---

I don't think the header of the nested function contains a syntax error, because the same header works as expected when not nested:
```vim
vim9script
def g:Bar()
enddef
defcompile
```
---

Could be on the todo list.  From `:h todo`:

   - <https://github.com/vim/vim/blob/d032f34a51c6722101626c4167dffecc427ac343/runtime/doc/todo.txt#L58-L60>
   - <https://github.com/vim/vim/blob/d032f34a51c6722101626c4167dffecc427ac343/runtime/doc/todo.txt#L116-L117>

##
##
##
# errors at `:h vim9`
## continuation line vs line continuation

The former is used 3 times; the latter 2 times.
Is there a (subtle) difference between the 2 terms?
If not, using both interchangeably is confusing.

## 81

> To improve readability there **must** be a space between the command and the #
> that starts a comment.

No error is raised if you don't write a space right after the `#` comment leader.
Therefore, shouldn't the doc use the word "should" instead of "must"?

## 99

> `:def` has no options like `:function` does: "range", "abort", "dict" or
> "closure".  A `:def` function always aborts on an error, does not get a range
> passed and cannot be a "dict" function.

The first sentence mentions closures, but not the second one.
Support for closures is in the todo list:

> - Make closures work:
>   - Create closure in a loop.  Need to make a list of them.

Maybe the doc could say:

> A `:def` function always aborts on an error, does not get a range
> passed, cannot be a "dict" function, and may be a closure.

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

## 124

> When using `:function` or `:def` to specify a new function inside a function,
> the function is local to the function.  **It is not possible to define a**
> **script-local function inside a function.** It is possible to define a global
> function, using the "g:" prefix.

Then the error should clearly explain this limitation:
```vim
vim9script
def FuncA()
    def s:FuncB()
    enddef
enddef
FuncA()
```
    Error detected while processing function <SNR>1_FuncA:
    line    1:
    E124: Missing '(': :FuncB()

It's not easy to understand what's wrong from this message.
Something like this would be better:

    Error detected while processing function <SNR>1_FuncA:
    line    1:
    E1234: cannot nest script-local function

## 131

> - Local to **the current scope and outer scopes** up to the function scope.

Not clear.
I would rather read "the current code block and outer code blocks".

Rationale: Coming from  legacy Vim script,  there is  no smaller scope  than the
function one.  The current sentence implies that there is one – which is true in
Vim9 script – without  specifying what it is.  It's explained  a little later at
`:h vim9-declaration`, but imo `:h vim9-scopes` should be understandable on its own.

## 141

> Global functions can be still be defined and deleted at nearly any time.  In
> Vim9 script script-local functions are defined once when the script is sourced
> and cannot be deleted or replaced.

Global functions can – indeed – be deleted with `:delfu`:
```vim
vim9script
def g:Func()
enddef
delfu g:Func
```
But isn't it a little confusing to delete a `:def` function with `:delfu`?
Shouldn't we use a `:deldef` command instead?

---

What does it mean for a script-local function to be defined "once"?

## 151

> Variables can be local to a script, function or code block:

What about the other scopes?  buffer-local, window-local, ...
```vim
vim9script
b:var = 123
```
## 186

From `:h vim9-declaration /exception`:

>     An existing variable cannot be assigned to with `:let`, since that implies a
>     declaration.  An exception is global variables: these can be both used **with**
>     and without `:let`, because there is no rule about where they are declared.

And from `:h vim9-declaration /value`

>     Global variables and user defined functions must be prefixed with "g:", also
>     at the script level. >
>             vim9script
>             let script_local = 'text'
>             **let g:global = 'value'**
>             let Funcref = g:ThatFunction

Something is wrong; while you can declare a global variable without `:let`, you can't with `:let` (nor can you assign it a value if it already exists):

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        let g:global = 'value'
    EOF
    )

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        let g:global = 'value'
    EOF
    )

    E1016: Cannot declare a global variable: g:global

I think it's like that since 8.2.1024 and 8.2.1028.

Btw, the same is true for `w:`, `b:`, `t:`, `v:`.

---

This is also true for environment variables.

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        let $VAR = 'test'
    EOF
    )

    E1016: Cannot declare an environment variable: $VAR = 'test'

And contrary to `g:`, `w:`, ..., you can't just drop the `:let`:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        $VAR = 'value'
    EOF
    )

    E1050: Colon required before a range

That's because `$` is parsed as a line specifier (the address of the last line).

As a workaround, use `setenv()`:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        setenv('VAR', 'test')
    EOF
    )

Maybe, this should be documented.

Note that the issue  only exists at the script level;  inside a `:def` function,
you can simply drop `:let`, just like with a global variable:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            $ENVVAR = 'foobar'
        enddef
        Func()
    EOF
    )

And you can even use `:unlet`:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            $ENVVAR = 'foobar'
            unlet $ENVVAR
        enddef
        Func()
    EOF
    )

## 190

> Variables cannot shadow previously defined variables.

Btw, what does this mean?
Does it mean that you can't re-declare a variable?

## 217

> "foobar"->Process()		" does NOT work
It *does* work:
```vim
vim9script
def Process(l: string): number
    return len(l)
enddef
echo "foobar"->Process()
```
---

> 'foobar'->Process()             " does NOT work

Again, it *does* work:
```vim
vim9script
def Process(l: string): number
    return len(l)
enddef
echo 'foobar'->Process()
```
---

Since `'foobar'->Process` and `"foobar"->Process()` both work, are those 2 lines still relevant:

> ("foobar")->Process()           " works

> ('foobar')->Process()           " works

## 229

From `:h vim9-declaration /cyclic`

> Note that while variables need to be defined before they can be used,
> **functions can be called before being defined**.  This is required to be able
> have cyclic dependencies between functions.  It is slightly less efficient,
> since the function has to be looked up by name.  And a typo in the function
> name will only be found when the call is executed.

I can't find a working example.
```vim
vim9script
A()
def A()
enddef
```
    E117: Unknown function: A

## 236

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

## 287

From `:h E1050`:

> recognized, it is required to put a colon before a range.  This will add
> "start" and print: >

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

## 308

> - No line break is allowed in the LHS of an assignment.  Specifically when
>   unpacking a list |:let-unpack|. This is OK: >
>         [var1, var2] =
>                 Func()

This does not work at the script level:
```vim
vim9script
def Func(): list<number>
    return [1, 2]
enddef
let var1: number
let var2: number
[var1, var2] =
        Func()
```
    Error detected while processing /proc/17235/fd/11:
    line    7:
    E15: Invalid expression: [var1, var2] =

Nor in a `:def` function.
```vim
vim9script
def Foo(): list<number>
    return [1, 2]
enddef
def Bar()
    let var1: number
    let var2: number
    [var1, var2] =
            Foo()
enddef
Bar()
```
    Error detected while processing function <SNR>1_Bar:
    line    3:
    E1004: white space required before and after '='

---

I reported the issue here:
<https://github.com/vim/vim/issues/6494#issuecomment-660781609>

But it was not fixed.
Sth else was fixed (list-unpacking at the script level).
Wait for the next update of the runtime  files; if the issue is not mentioned in
the todo list by that time, open a report.

## 316

> - No line break is allowed in between arguments of an `:echo`, `:execute` and
>   similar commands.  This is OK: >
>         echo [1,
>                 2] [3,
>                         4]

This does not work at the script level:
```vim
vim9script
echo [1,
        2] [3,
              4]
```
    Error detected while processing /proc/15664/fd/11:
    line    3:
    E111: Missing ']'
    line    4:
    E1050: Colon required before a range

Nor in a `:def` function:
```vim
vim9script
def Func()
    echo [1,
            2] [3,
                  4]
enddef
Func()
```
    Error detected while processing function <SNR>1_Func:
    line    2:
    E111: Missing ']'

I can't even make it work in legacy without any line break:

    :echo [1, 2] [3, 4]
    E111: Missing ']'~

I think an operator is missing between the lists.
The following works at the script level:
```vim
vim9script
echo [1,
        2] + [3,
                4]
```
And in a `:def` function:
```vim
vim9script
def Func()
    echo [1,
            2] + [3,
                    4]
enddef
Func()
```
---

But if a binary operator is missing, it begs the question:

> This does not work: >
>      echo [1, 2]
>              [3, 4]

What doesn't work exactly?
If I add a `+` operator, the command works at the script level:
```vim
vim9script
echo [1, 2]
      + [3, 4]
```
And in a `:def` function:
```vim
vim9script
def Func()
    echo [1, 2]
          + [3, 4]
enddef
Func()
```
## 338

> No :append, :change or :insert ~
>
> These commands are too quickly confused with local variable names.

I would add `:xit`  to this list. `x` can also be quickly  confused with a local
variable name.  If one wants to run  the legacy `:x`, they can still use `:exit`
which is more readable anyway.

Also, something should be said about the variable names `b`, `g`, `s`, `t`, `v`, `w`.
You can assign a value to them, either at the script level:
```vim
vim9script
let b = 123
```
Or in a `:def` function:
```vim
vim9script
def Func()
    let b = 123
enddef
defcompile
```
You can declare them at the script level:
```vim
vim9script
let b: number
b = 123
```
But you can't declare them in a `:def` function:
```vim
vim9script
def Func()
    let b: number
    b = 123
enddef
defcompile
```
    Error detected while processing function <SNR>1_Func:
    line    1:
    E1016: Cannot declare a buffer variable: b

The error message is different for `s`:

    Error detected while processing function <SNR>1_Func:
    line    1:
    E1054: Variable already declared in the script: s

And for `v`:

    Error detected while processing function <SNR>1_Func:
    line    1:
    E1001: variable not found: v: number

This is inconsistent.  Either it should work in a `:def` function, or it should fail at the script level.

Also, maybe Vim should raise a more telling error message.  It's not clear what's wrong.  This would be more clear:

    E1234: Cannot declare a variable whose name matches a valid variable scope~

Maybe not that *exact* message, but something similar.

## 343

> Comparators ~
>
> The 'ignorecase' option is not used for comparators that use strings.

We can still use `=~#` and `=~?`:
```vim
vim9script
set ic
def Func()
    let str = 'aBc'
    echo str =~? 'abc'
enddef
Func()
```
    v:true

Isn't `=~#` redundant in Vim9 script?  It seems to give the same results as `=~`...

Maybe `=~#` and `=~?` should be disallowed in Vim9 script.
I think it would be in line with the secondary goal of Vim9 script which is to avoid Vim-specific constructs.

## 401

> The boolean operators "||" and "&&" do not change the value: >

I don't understand this sentence.
Which value?  The truthfulness of the statement?
`||` and `&&` *do* change the resulting truthfulness of an expression containing
operands used as booleans.

---

> [] && 2  == []

This doesn't work:
```vim
vim9script
if [] && 2  == []
    echo 'this is true'
endif
```
    Error detected while processing ...
    line    2:
    E745: Using a List as a Number
```vim
vim9script
def Func()
    if [] && 2  == []
        echo 'this is true'
    endif
enddef
Func()
```
    Error detected while processing function <SNR>1_Func:
    line    1:
    E1072: Cannot compare list with number

Also, why are the 2 error messages different?

## 410

> When using `..` for string concatenation the arguments are always converted to
> string. >
>         'hello ' .. 123  == 'hello 123'
>         'hello ' .. v:true  == 'hello true'

The first example works, but not the second one:
It needs to be adapted:

    'hello ' .. v:true  == 'hello v:true'
                                  ^^
                                  this is missing
```vim
vim9script
if 'hello ' .. v:true  == 'hello v:true'
    echo 'this is true'
endif
```
    this is true

## 424

> Ex command ranges need to be prefixed with a colon. >
>   	->		" legacy Vim: shifts the previous line to the right
> 	->func()	" Vim9: method call in continuation line
> 	:->		" Vim9: shifts the previous line to the right
>
> 	%s/a/b		" legacy Vim: substitute on all lines
> 	x = alongname
> 	     % another	" Vim9: line continuation without a backslash
> 	:%s/a/b		" Vim9: substitute on all lines
> 	'text'->func()	" Vim9: method call
> 	:'t		" legacy Vim: jump to mark m

There is a pattern here:

   1. what did this token mean in Vim legacy?
   2. what does it mean in Vim9?
   3. how to get back the original meaning in Vim9?

But the pattern is not respected at the end.
I would rewrite the paragraph like this:

> Ex command ranges need to be prefixed with a colon. >
>   	->		" legacy Vim: shifts the previous line to the right
> 	->func()	" Vim9: method call in continuation line
> 	:->		" Vim9: shifts the previous line to the right
>
> 	%s/a/b		" legacy Vim: substitute on all lines
> 	x = alongname
> 	     % another	" Vim9: **modulo in continuation line**
> 	:%s/a/b		" Vim9: substitute on all lines

> 	't            	" legacy Vim: jump to mark m
> 	'text'->func()	" Vim9: method call **on string expression**
> 	:'t		" Vim9: jump to mark m

Note the new empty line between the second and third blocks to improve the readability.
And note the new description of this assignment:

    x = alongname
         % another  " Vim9: modulo in continuation line

Which is more consistent with:

    ->func()        " Vim9: method call in continuation line

---

Something is wrong in the `:'t` example; it just doesn't work:
```vim
vim9script
setline(1, ['foo', 'bar', 'baz'])
norm! 2G2|mt
:'t
```
    Error detected while processing ...
    line    4:
    E492: Not an editor command: :'t
```vim
vim9script
def Func()
    setline(1, ['foo', 'bar', 'baz'])
    norm! 2G2|mt
    :'t
enddef
Func()
```
    Error detected while processing function <SNR>1_Func:
    line    3:
    E476: Invalid command: 't

---

I would add a gotcha about the fact  that you can *not* omit `s:` when calling a
script-local function from a `:fu` function.
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

## 444

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

## 492

> NOTE: It is possible to nest `:def` inside another
> `:def`, but it is not possible to nest `:def` inside
> `:function`, for backwards compatibility.

I *can* nest `:def` inside `:fu`:
```vim
vim9script
fu Foo()
    def Bar()
        echo 'bar'
    enddef
    call Bar()
endfu
Foo()
```
    bar
```vim
vim9script
fu Foo()
    def Bar()
        echo 'bar'
    enddef
endfu
Foo()
Bar()
```
    bar

## 504

> If the script the function is defined in is Vim9 script, then script-local
> variables can be accessed without the "s:" prefix.  They must be defined
> before the function is compiled.  If the script the function is defined in is
> legacy script, then script-local variables must be accessed with the "s:"
> prefix.

I would re-write this paragraph like so:

> If the function is defined in a Vim9 script, then script-local variables can
> be accessed without the "s:" prefix.  They must be defined before the function
> is compiled.  If the function is defined in a legacy script, then script-local
> variables must be accessed with the "s:" prefix.

Easier to understand.

## 543

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

## 651

From `:h :vim9 /common`:

>     In Vim9 script the global "g:" namespace can still be used as before.  And the
>     "w:", "b:" and "t:" namespaces.  These have in common that variables are not
>     declared and they can be deleted.

Maybe environment variables should be mentioned as well.

Also, I would rewrite the whole paragraph like this:

>     In Vim9 script the global "g:" namespace can still be used as before.  And the
>     "w:", "b:", "t:", and "$" namespaces.  These have in common that their
>     variables cannot be declared but can be deleted.
>     For variables which are local to a script, function or code block, the opposite
>     is true.  They can be declared but cannot be deleted.

## 674

>     Alternatively, an export statement can be used to export several already
>     defined (otherwise script-local) items: >
>             export {EXPORTED_CONST, someValue, MyFunc, MyClass}

Does not work:
```vim
vim9script
const EXPORTED_CONST = 123
let someVariable = 'test'
export {EXPORTED_CONST, someVariable}
```
    E1043: Invalid command after :export

```vim
vim9script
let someVariable = 'test'
export someVariable
```
    E1043: Invalid command after :export

There is a test which suggests that `E1043` is expected when trying to export one item:
https://github.com/vim/vim/blob/bc6fcbe4ce52bc48c3d77b24086acc61ed3333bc/src/testdir/test_vim9_script.vim#L1143

But I didn't find any test suggesting that `E1043` was expected when trying to export *several* items.  If it is working as intended, then the documentation looks wrong.

---

Also, I don't understand what "(otherwise script-local)" means here.

## 714

> The `import` commands are executed when encountered.
> If that script  (directly or indirectly) imports the current  script, then items
> defined after the `import` won't be processed yet.
> Therefore, cyclic imports can exist, but may result in undefined items.

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

## 789

>     The error can be given at compile time, no error handling is needed at runtime.

If  the function  contains a  type error,  it's still  installed (like  a legacy
function), but its body is empty.

This is neat, and maybe it should be documented.
If a  legacy function  contains syntax/type errors,  and was  invoked frequently
(e.g. `InsertCharPre` autocmd),  the same  errors were raised  repeatedly.  This
shoud not happen with a `:def` function.

##
# missing doc at `:h vim9`
## Vim9: "is#" and "is?" don't work inside a ":def" function

**Describe the bug**

`is#` doesn't work inside a `:def` function.

**To Reproduce**

Run this shell command:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            echo 'test' is# 'test'
        enddef
        defcompile
    EOF
    )

`E15` is raised:

    Error detected while processing function <SNR>1_Func:
    line    1:
    E15: Invalid expression:  is# 'test'

**Expected behavior**

No error is raised.

**Environment**

 - Vim version: 8.2 Included patches: 1-1126
 - OS: Ubuntu 16.04.6 LTS
 - Terminal: XTerm(356)

**Additional context**

`is#` and `is?` work as expected if you replace them with `is`:
```vim
vim9script
def Func()
   echo 'test' is 'test'
enddef
defcompile
```
Or if you run the code inside a legacy function:
```vim
vim9script
fu Func()
   echo 'test' is# 'test'
endfu
defcompile
```
Or if you run the code at the script level:
```vim
vim9script
echo 'test' is# 'test'
```
---

Update: I'm not sure this is really a bug.

>     These ones are not backwards compatible, we'll fix this in Vim9 script:
>     Also, "'' == 0" evaluates to true, which isn't nice.
>     Add "===" to have a strict comparison (type and value match).
>     Add "==*" (?) to have a value match, but no automatic conversion, and v:true
>     equals 1 and 1.0, v:false equals 0 and 0.0.?

I suspect Bram wants to get rid of `is#` and `is?` in Vim9, in favor of new comparison operators like `===`.
But even so, the documentation should probably mention this pitfall at `:h vim9-differences`.

See also `:h vim9 /ignorecase`:

>     Comparators ~
>
>     The 'ignorecase' option is not used for comparators that use strings.

## can't use ":breakadd func" with a ":def" function

Can we?  Last time I tried, it didn't work.

It's working as intended.
Maybe `:breakadd` doesn't work because it can't work with a compiled function...
If so, it should be documented at `:h vim9-differences`.

---

And what about `:profile`?

## can't declare a register inside a ":def" function

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            let @a = 'text'
        enddef
        Func()
    EOF
    )

    Error detected while processing function <SNR>1_Func:
    line    1:
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

---

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            let @/ = 'text'
        enddef
        Func()
    EOF
    )

    Error detected while processing function <SNR>1_Func:
    line    1:
    E354: Invalid register name: '/'

This error looks wrong.  It should be `E1066`, not `E354`.

## can get the definition of a `:def` function with `:fu`

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def g:Func()
            echo 'test'
        enddef
    EOF
    )

    :fu Func
        def Func()
     1          echo 'test'
        enddef

Is it intended?

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

#
##
##
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

    :call range(1, winnr('$'))->map({_,v -> win_execute(v, '" set some option')})

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

# Feature request: add an `-R` flag to `bind-key` to repeat only 1 key

I would like to make more key bindings repeatable.
The current way to do so is to pass the `-r` flag to `bind-key`.
Unfortunately, it frequently leads to unexpected behavior.

Here's one example.
I have these repeatable key bindings to resize panes:

set -g repeat-time 1000
bind -r C-h resizep -L 5
bind -r C-j resizep -D 5
bind -r C-k resizep -U 5
bind -r C-l resizep -R 5

I would like to make `)` and `(` repeatable, and so I install these key bindings:

bind -r ( switchc -p
bind -r ) switchc -n

I frequently want to have a look at a window in another session, so I press the prefix key followed by `)` to focus the next session, then I press `)` again to focus my main session again (I only have 2 sessions).

Update: Ah crap. It's more complex. You don't want `-R` to repeat only 1 key, but a particular subset of keys.
Do we want sth like `vim-submode` but for Tmux?

##
# copy-pipe

`copy-pipe` sometimes truncates the selection when piping it to `xsel(1x)`.

I have this key binding which worked well when I was using urxvt as my terminal:

bind -T copy-mode-vi y send -X copy-pipe-and-cancel 'xsel -i --clipboard'

Its purpose is to copy the tmux selection into the X clipboard selection.

Now, I'm using st, and I've noticed that the text in the clipboard is truncated after approximately 375 characters.
I think the real number depends on the terminal window width and/or the font size, but I could be wrong.

Here's a MWE which I've tested against Ubuntu 16.04, as well as Ubuntu 18.04 (in a virtual machine).

    $ sudo apt-get update
    $ sudo apt-get install curl git libx11-dev libxft-dev pkg-config xsel
    $ git clone https://git.suckless.org/st
    $ cd st
    $ make
    $ curl -LO http://invisible-island.net/datafiles/current/terminfo.src.gz
    $ gunzip terminfo.src.gz
    $ tic -sx terminfo.src
    $ ./st

# don't include that section in your bug report

    $ cd ..
    $ git clone https://github.com/tmux/tmux
    $ cd tmux

# would this command have worked instead? `$ sudo aptitude build-dep tmux`

    $ sudo apt-get install automake libevent-dev libncurses5-dev
    $ sh autogen.sh
    $ ./configure
    $ make

    $ tmux -Lx -f/dev/null new
    $ tmux set -gw mode-keys vi
    $ tmux bind -T copy-mode-vi y send -X copy-pipe-and-cancel 'xsel -i --clipboard'
    $ vim -Nu NONE
    :echo repeat('x', 370) . ' this text should not be truncated'
    C-b [
    kVkkkkk
    y

The Vim command:

    :echo repeat('x', 370) . ' this text should not be truncated'

will output a string of 370 `x` characters on the command-line, followed by the text ` this text should not be truncated`. The purpose of the motions in copy-mode (`kvkkkkk`) is to select all the characters in this string.

When I try to paste the contents of the X clipboard (in a Vim compiled with the clipboard feature, one can do so by pressing `"+p`), I correctly get 370 characters `x`, but ` this text should not be truncated` is truncated right after ` this`.

## Possible cause

I think the issue is due to an interaction between `copy-pipe` and the st terminal.

It's not due to `copy` (without `-pipe`), because this key binding always works as expected:

    $ tmux bind -T copy-mode-vi y send -X copy-selection

That is, it copies the previous long string in a tmux buffer, without truncation.

And it's specific to st, because I can't reproduce in xterm.

## Wrong hypotheses
### The issue is in `xsel(1X)`

At first, I thought that the issue was due to `xsel(1x)`, because the latter had [a bug](https://github.com/kfish/xsel/issues/13) in the past, which truncated the selection after 4000 characters. It was fixed by [this PR](https://github.com/kfish/xsel/pull/16).

But this old bug can't be the cause of the current issue, because I've recompiled `xsel(1x)` to get the most recent version. Besides, I can reproduce with `xclip(1)` too.

In fact, it doesn't even matter to which command you pipe the tmux selection. You can use a non existing command, and tmux will send it to the X clipboard selection (but still truncate it after around 375 characters).
I checked this with the following key binding:

    $ tmux bind -T copy-mode-vi y send -X copy-pipe-and-cancel 'not_a_command'
                                                                ^^^^^^^^^^^^^

I have no idea what tmux is piping the selection to, though.

### ?

Make some tests with any of these key bindings:

    $ tmux bind -T copy-mode-vi Z send -X copy-pipe-and-cancel 'xclip -selection clipboard'
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe-and-cancel 'xsel -i --clipboard'
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe 'xclip -selection clipboard'
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe 'xsel -i --clipboard'
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe-and-cancel 'tee /tmp/file' \\\; run 'xsel -i --clipboard </tmp/file'

I think the  issue is in an interaction  between `copy-pipe[-and-cancel]` and st.
Indeed, I can't reproduce with `cat(1)` :

    bind -T copy-mode-vi Z send -X copy-pipe 'cat >/tmp/test'

### ?

Find a MWE.

It seems the limit is 376 characters.
Run this:

    :echo repeat('a', 375) . 'bb'

Enter copy-mode and try to copy the 377 characters.
Paste it in a buffer (`""p`), and you'll see that the last `b` is replaced with a backtick.
You can add as many `b` as you want; when you paste, you'll only get one `b` + a backtick.
Weirdly enough, if  you try to reproduce  by writing the text in  a file, then
cat'ing  it in  the shell,  you'll  see that  the  limit is  increased to  379
characters.

But it can't be this, because we've updated xsel, and because we can reproduce
with xclip too.

Update:
Try to install a key binding which  would first simply copy the selection in a
tmux buffer:

    $ tmux bind -T copy-mode-vi Z send -X copy-selection-and-cancel

Now, try to make  the key binding manually invoke `xsel(1x)`  or `xclip(1)` in a
second step.

Does it work?
If it does, you've found a workaround (still, maybe you should report the issue).
If it doesn't, try to install a  key binding which would just call `xsel(1x)` or
`xclip(1)` with a long text.
Does it succeed in populating the clipboard selection?
If it doesn't you've found a simpler MWE.
If it does, this is weird... keep investing.

    ✘
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe-and-cancel 'tee /tmp/file' \\\; run 'xsel -i --clipboard </tmp/file'
    ✔
    $ tmux bind Z run 'xsel -i --clipboard </tmp/file'

MWE:

    $ curl -LO http://invisible-island.net/datafiles/current/terminfo.src.gz
    $ gunzip terminfo.src.gz
    $ tic -sx terminfo.src
    $ git clone https://git.suckless.org/st
    $ cd st
    $ make
    $ ./st
    $ tmux -Lx -f/dev/null new
    $ tmux set -gw mode-keys vi
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe-and-cancel 'tee /tmp/file' \\\; run 'xsel -i --clipboard </tmp/file'
    $ vim -Nu NONE
    :echo repeat('a', 375) . repeat('b', 10)
    C-b [
    kkkk0
    Vjjj
    Z

Note that `set -gw mode-keys vi` is necessary to make sure that, in copy-mode,
tmux uses the emacs key table, and not the vi one.
This is  because tmux chooses between the  emacs key table vs the vi one based on
the value of the `mode-keys` option.
Also, the motions to select the text depend  on the font size and the width of
the terminal window (and don't press `v` to start the selection, but `V`).
Finally, `tee(1)`  is provided  by the  coreutils package, which  seems to  be a
fundamental package. So, it should be ok to use it in a MWE.

### ?

Interestingly enough, the next key binding works:

    $ tmux bind -T copy-mode-vi Z send -X cancel \\\; run 'xsel -i --clipboard </home/user/Vcs/tmux/COPYING'

Which seems to  indicate that the issue  is *not* linked to copy  mode, but to
*some* commands in copy mode.

Try to update the previous MWE, to reduce the difference between these commands
(the first one must work, but not the second):

    $ tmux bind -T copy-mode-vi Z send -X cancel \\\; run 'xsel -i --clipboard </home/user/Vcs/tmux/COPYING'
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe-and-cancel 'tee /tmp/file' \\\; run 'xsel -i --clipboard </tmp/file'

    ⇒

    $ tmux bind -T copy-mode-vi Z send -X cancel \\\; run 'xsel -i --clipboard </tmp/file'
    $ tmux bind -T copy-mode-vi Z send -X copy-pipe 'tee /tmp/file' \\\; run 'xsel -i --clipboard </tmp/file'

to continue...

### ?

I found a workaround:

    bind-key -T copy-mode-vi y run "tmux send -X copy-pipe-and-cancel 'xsel -i --clipboard';"
                                                                                           ^

Notice the semicolon at the end. It fixes the issue.
This key binding should be roughly equivalent:

    bind-key -T copy-mode-vi y send -X copy-pipe-and-cancel 'xsel -i --clipboard' \; run ':'
                                                                                          ^

And yet, it doesn't fix the issue. Why?
And why do we need `;` in the first working key binding?

Note that we can't use `;` in the second key binding, because tmux would complain:

    $ tmux bind-key -T copy-mode-vi y send -X copy-pipe-and-cancel 'xsel -i --clipboard' \\\; run ';'
    usage: run-shell [-b] [-t target-pane] shell-command~

But `:` should have the same effect; i.e. none.
From `man bash /SHELL BUILTIN COMMANDS`:

> : [arguments]
>        No effect; the command does nothing beyond  expanding  arguments
>        and  performing any specified redirections.  A zero exit code is
>        returned.

### ?

Ask this question to nicm:

> If it's not a bug in tmux, could you explain:

>    - why do I need to add a trailing `true(1)` statement?
>    - why does the seemingly equivalent workaround fail?
>    - is it a general issue;
>      i.e. do I need a trailing `true(1)` statement + a `run-shell`, every time I use copy-pipe?

### ?

In Vim, it seems that st doesn't need xsel.
How is that even possible?

It even works when we pipe the tmux selection to a non-existing command

    bind -T copy-mode-vi y send -X copy-pipe-and-cancel 'not_a_command'

### ?

How to use OSC 52 to set the clipboard with arbitrary text?

    $ printf '\e]52;c;%s\x07' $(printf 'hello' | base64)

This should work in tmux too, provided that the outer terminal has the `Ms` capability.

Also, to better understand OSC 52, read this:
<https://www.mail-archive.com/tmux-users%40lists.sourceforge.net/msg05928.html>
<https://sunaku.github.io/tmux-yank-osc52.html>
<https://medium.freecodecamp.org/tmux-in-practice-integration-with-system-clipboard-bcd72c62ff7b>

Explanation regarding the special argument `-` (used in a command in one of the previous links):
<https://unix.stackexchange.com/questions/41828/what-does-dash-at-the-end-of-a-command-mean>

Security concern:
<https://bugzilla.gnome.org/show_bug.cgi?id=795774#c2>
<https://github.com/mintty/mintty/issues/258>

See also: `OSC Ps ; Pt ST /Ps = 5 2`

---

Issue: if one day we need to sync  a remote and local clipboards via OSC 52, and
we use st, we're limited to around 378 characters.
How to increase this limit?

Solution:

    $ sed -i.bak 's/^\(#define\s\+ESC_BUF_SIZ\s\+(\)[0-9]*\(\*UTF_SIZ)\)/\11024\2/' ~/GitRepos/st/st.c
                                                                           ├──┘
                                                                           └ the default value is 128

Adapt the new max to the max used by the yank script:

74994

Btw, where does this max come from?

Answer: Read the script.
It says that the sequence has a header of 7 bytes (`\e]52;c;`) plus a footer of 1 byte (`\a`) – btw, that's not true in tmux, where those are a little longer – so 99992 bytes remains out of a max of 100000 bytes.
And it mentions a formula (`4 * ceil(n/3)`) which I think gives the size of the base64 encoding of an input string of size `n`. So, 74994 is the input size to which the encoding is 99992 bytes.

And if you wonder where does the 100000 come from, I think it's an arbitrary max size followed by tmux.
<https://www.mail-archive.com/tmux-users%40lists.sourceforge.net/msg05950.html>
In the previous comment, sunaku mentions a link (now dead), which I guess mentions this limit.
But nicm explains that xterm doesn't define any limit.
So, 100000 is an arbitrary number.

### ?

To understand st weird behavior regarding the clipboard, read this:

<https://github.com/tmux/tmux/issues/1119>
<https://github.com/tmux/tmux/issues/1407>

### ?

Make some tests to check our understanding of what happens with st.
That is, in urxvt, `xsel(1x)` should be running to own the selection.
But in st,  `xsel(1x)` should not be running,  since st is the last  one to have
written in the X clipboard; so st  should be the owner, `xsel(1x)` is not needed
anymore, therefore it should not be running.

Update: Yes, it's confirmed.
Run tmux in st, then run `ls(1)`, and copy the output in tmux copy mode.
Finally, run `$ ps aux | grep xsel`: there's no xsel process.

Repeat the experiment in urxvt. This time, there is a xsel process.

### ?

Document that if  the clipboard doesn't contain what you  expect (after using an
OSC 52 sequence), you should inspect all the selections:

    $ xsel -p (primary)
    $ xsel -s (secondary)
    $ xsel -b (clipboard)

### final solution

We've fixed the issue by increasing the value `ESC_BUF_SIZ` in `~/GitRepos/st/st.c:37`

By default, it's:

    128 * UTF_SIZ
    =
    128 * 4
    =
    512

In the patch `~/.config/st/patches/10_big_clipboard.diff`, we increase it to:

    25000 * UTF_SIZ
    =
    100000

Why `100000`?

Because after  a bug  report was  submitted to  nicm (tmux  dev), tmux  allows a
maximum size of 100K bytes for an escape sequence.

Relevant excerpts from the original issue:

Question:

>     However, since the maximum length of an OSC 52 escape sequence is
>     **100,000** bytes[1] and the patched tmux's DCS escape sequence length
>     limit is 32772 bytes (as observed above), how would you recommend
>     sending a maximum-length OSC 52 escape sequence through tmux?

Answer:

>     Actually looking at xterm it doesn't have a limit for this escape
>     sequence, we can probably make tmux's a lot bigger so long as we reduce
>     it back to 32 bytes after the sequence is done.

<https://www.mail-archive.com/tmux-users%40lists.sourceforge.net/msg05949.html>
<https://www.mail-archive.com/tmux-users%40lists.sourceforge.net/msg05950.html>

---

Document all of this in `~/.config/st/patches/README.md`.

##
# `#{pane_status_dead}` sometimes wrongly empty
### Issue description

To reproduce, run these shell commands:

    $ cat <<'EOF' >/tmp/tmux.conf
    bind -T copy-mode-vi x send -X copy-pipe-and-cancel "xargs -I {} tmux run 'xdg-open \"{}\"'"
    EOF
    $ tmux -Lx -f/tmp/tmux.conf
    $ ls | tmux splitw -dI \; set -w remain-on-exit on \; splitw 'aaa'
    C-b :display '#{pane_dead_status}'

The output of the last command is empty, but it should be `127`.

I don't  know why, but  the issue seems  to be due to  this key binding  (and in
particular to the double quotes surrounding the url passed to `xdg-open(1)`):

    bind -T copy-mode-vi x send -X copy-pipe-and-cancel "xargs -I {} tmux run 'xdg-open \"{}\"'"
                                                                                        ^^  ^^

Update:
Forget about this bug for the moment.
I can't reproduce it reliably.
It depends on sth else; I don't know what.

### Required information

- `$ tmux -V`: tmux next-3.1
- `$ uname -sp`: Linux x86_64
- terminal: xterm
- `$TERM` outside tmux: xterm-256color
- `$TERM` inside tmux: screen
- logs from `$ tmux -vv -Lx -f/tmp/tmux.conf`:

##
# E749

`E749` is sometimes raised when leaving Ex mode

- `vim --version`:      VIM - Vi IMproved 8.1  Included patches: 1-1119
- Operating system:     Ubuntu 16.04.6 LTS
- Terminal emulator:    rxvt-unicode v9.22
- Terminal multiplexer: tmux 2.9
- `$TERM`:              tmux-256color
- Shell:                zsh 5.7.1-dev-0 (x86_64-pc-linux-gnu)

**Describe the bug**

If a function which contains an empty line is called when entering or leaving Ex mode, `E749` is raised, but only if Ex mode was entered via `gQ`, not `Q`.

**To Reproduce**

E749: empty buffer

    $ vim -Nu NONE +'cno <expr> <cr> Func()' +'fu Func()

        return "\<cr>"
    endfu
    '

In the past, [E501 was raised instead of E749](https://raw.githubusercontent.com/lacygoill/CmdlineEnter_gif/master/E501.gif).

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

