<https://github.com/vim/vim/blob/master/runtime/doc/vim9.txt>
<https://github.com/vim/vim/blob/master/runtime/doc/todo.txt>

# Vim9
## Plan

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
    com! -bar -complete=customlist,s:def_complete -nargs=? Def exe s:def(<q-args>)
    fu s:def_complete(argLead, _l, _p) abort
        let argLead = substitute(a:argLead, '^\Cs:', '<SNR>[0-9]\\\\\\{1,}_', '')
        return getcompletion(argLead, 'function')->map('substitute(v:val, "($\\|()$", "", "")')
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

##
## bug: can delete a function-local or block-local function nested in a legacy function

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

   > Global functions can be still be defined and deleted at nearly any time.  In
   > Vim9 script script-local functions are defined once when the script is sourced
   > and cannot be deleted or replaced.

To this:

   > Global functions can be still be defined and deleted at nearly any time.  In
   > Vim9 script, script-local functions are defined once when the script is sourced
   > and cannot be deleted or replaced.  Similarly, a function local to a function
   > is defined when the latter is run, and cannot be deleted or replaced.
   > The same is true fo a function local to a block.

## bug: inconsistent error message when trying to delete local function nested in ":def" function

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
If the outer function is a `:fu`, no  error is raised; no matter the type of the
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
If the outer function is a `:fu`, no  error is raised; no matter the type of the
inner function.

---

No issue for an imported function:
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
delfu s:Imported
```
    E1084: Cannot delete Vim9 script function s:Imported

This is consistent with:
```vim
vim9script
def Func()
enddef
delfu s:Func
```
    E1084: Cannot delete Vim9 script function s:Imported

## bug: type casting doesn't work at the script level

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        g:two = 2
        let l: list<number> = [1, <number>g:two]
    EOF
    )

    E15: Invalid expression: <number>g:two]~

Update:  It's not necessary right now.
Why?

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        g:two = 2
        let l: list<number> = [1, g:two]
    EOF
    )
    ✔
    no error even though "g:two" was not cast to a number;
    Shouldn't "[1, g:two]" contain a mix of "<number>" and "<any>"?

    If it is a bug, note that a similar issue was fixed:  https://github.com/vim/vim/issues/6712

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        g:two = 2
        def Func()
            let l: list<number> = [1, g:two]
        enddef
        Func()
    EOF
    )

    E1012: type mismatch, expected list<number> but got list<any>~
    this is expected

It can't be due to the fact there is no type checking at the script level.
There *is*:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        let l: number = 'string'
    EOF
    )

    E1012: type mismatch, expected number but got string~

I think that – at the script level –  Vim only checks the type of the first item
in a list.  That was fixed – in a `:def` function – by the patch 8.2.1407.

---

I'm not sure this is a bug, because `:h type-casting` only mentions compiled code.
Still, it would be more consistent if it also worked at the script level.
Although, would it make sense?

##
## ?

According to the help, these functions accept a funcref as an argument:

  - `:h call()`
  - `:h eval()`
  - `:h filter()`
  - `:h map()`
  - `:h search()`
  - `:h searchpair()`
  - `:h setqflist()`
  - `:h sort()`
  - `:h substitute()`
  - `:h timer_start()`

Do they also accept a function name?
```vim
fu Func()
    echo 'working'
endfu
call call('Func', [])
```
    working
```vim
fu Func()
    return 'working'
endfu
echo 'Func'->string()->eval()()
```
    E15: Invalid expression: )
```vim
fu MyFilter(i, v)
    return a:v =~ 'keep'
endfu
echo ['removeme', 'keepme', 'deleteme']->filter('MyFilter')
```
    E121: Undefined variable: MyFilter
```vim
fu MyMap(i, v)
    return a:v * 100
endfu
echo [1, 2, 3]->map('MyMap')
```
    E121: Undefined variable: MyMap
```vim
call setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
fu MySkip()
    return synstack('.', col('.'))
        \ ->map({_, v -> synIDattr(v, 'name')})
        \ ->match('\ccomment') != -1
endfu
echo search('\<endif\>', '', 'MySkip')
```
    2
    ✘
    should be 3
```vim
call setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
fu MySkip()
    return synstack('.', col('.'))
        \ ->map({_, v -> synIDattr(v, 'name')})
        \ ->match('\ccomment') != -1
endfu
echo searchpair('\<if\>', '', '\<endif\>', '', 'MySkip')
```
    E121: Undefined variable: MySkip
    btw, why is "MySkip" evaluated as a variable name here, but not in search()
```vim
fu Func(info)
    return repeat(['test'], 100)
endfu
call setqflist([], 'r', {'lines': v:oldfiles, 'efm': '%f', 'quickfixtextfunc': 'Func'})
cw
```
    ✔
```vim
fu Func()
    echo ['bbb', 'aaa']->sort('MySort')
endfu
fu MySort(line1, line2)
    return a:line1 > a:line2 ? 1 : -1
endfu
call Func()
```
    ['aaa', 'bbb']
```vim
fu MyRep()
    return 1
endfu
echo substitute('aaa', '.', MyRep, 'g')
```
    E121: Undefined variable: MyRep
```vim
fu MyCb(_)
    echom 'my callback'
endfu
call timer_start(0, 'MyCb')
```
    my callback

Conclusion:  Out of the 10 functions, only 4 accept a function name instead of a funcref:

   - `call()`
   - `setqflist()`
   - `sort()`
   - `timer_start()`

## ?

When a function accepts a function name as an argument, how does it work in Vim9
script?  That is, does it work *without* quotes?  Does it work *with* quotes?
```vim
vim9script
def MyCall()
    echo 'my call'
enddef
def Func()
    call('MyCall', [])
enddef
Func()
```
    my call
```vim
vim9script
def MyCall()
    echo 'my call'
enddef
def Func()
    call(MyCall, [])
enddef
Func()
```
    my call
```vim
vim9script
def MyQftf(info: any): any
    return repeat(['test'], 100)
enddef
def Func()
    setqflist([], 'r', {'lines': v:oldfiles, 'efm': '%f', 'quickfixtextfunc': 'MyQftf'})
    cw
enddef
Func()
```
    ✔
```vim
vim9script
def MyQftf(info: any): any
    return repeat(['test'], 100)
enddef
def Func()
    setqflist([], 'r', {'lines': v:oldfiles, 'efm': '%f', 'quickfixtextfunc': MyQftf})
    cw
enddef
Func()
```
    ✔
```vim
vim9script
def Func()
    echo ['bbb', 'aaa']->sort('MySort')
enddef
def MySort(line1: string, line2: string): number
    return line1 > line2 ? 1 : -1
enddef
Func()
```
    E1030: Using a String as a Number
```vim
vim9script
def Func()
    echo ['bbb', 'aaa']->sort(MySort)
enddef
def MySort(line1: string, line2: string): number
    return line1 > line2 ? 1 : -1
enddef
Func()
```
    ['aaa', 'bbb']
```vim
vim9script
def MyCb(_: number)
    echom 'my callback'
enddef
def Func()
    timer_start(0, expand('<SID>') .. 'MyCb')
enddef
Func()
```
    my callback
```vim
vim9script
def MyCb(_: number)
    echom 'my callback'
enddef
def Func()
    timer_start(0, MyCb)
enddef
Func()
```
    my callback

---

Repeat the tests at the script level.
```vim
vim9script
def MyCall()
    echo 'my call'
enddef
call('MyCall', [])
```
    my call
```vim
vim9script
def MyCall()
    echo 'my call'
enddef
call(MyCall, [])
```
    my call
```vim
vim9script
def MyQftf(info: any): any
    return repeat(['test'], 100)
enddef
setqflist([], 'r', {'lines': v:oldfiles, 'efm': '%f', 'quickfixtextfunc': 'MyQftf'})
cw
```
    ✔
```vim
vim9script
def MyQftf(info: any): any
    return repeat(['test'], 100)
enddef
setqflist([], 'r', {'lines': v:oldfiles, 'efm': '%f', 'quickfixtextfunc': MyQftf})
cw
```
    ✔
```vim
vim9script
def MySort(line1: string, line2: string): number
    return line1 > line2 ? 1 : -1
enddef
echo ['bbb', 'aaa']->sort('MySort')
```
    E1030: Using a String as a Number
```vim
vim9script
def MySort(line1: string, line2: string): number
    return line1 > line2 ? 1 : -1
enddef
echo ['bbb', 'aaa']->sort(MySort)
```
    ['aaa', 'bbb']
```vim
vim9script
def MyCb(_: number)
    echom 'my callback'
enddef
timer_start(0, expand('<SID>') .. 'MyCb')
```
    my callback
```vim
vim9script
def MyCb(_: number)
    echom 'my callback'
enddef
timer_start(0, MyCb)
```
    my callback

---

Conclusions:

   - we *can* omit the quotes for `call()`, `setqflist()`, `timer_start()`
   - we can *not* omit the quotes for `sort()`

Let's assume that the quotes are meant to be still allowed (that's my impression
after reading `:h vim9 /Omitting function()`):  we should be able to omit quotes
for `sort()` (at the script level, and in a `:def` function).

## ?

When a function which  accepts a funcref as argument but not  a function name is
used in Vim9 script, what happens?  Can we now pass it a function name *without*
quotes?  *With* quotes?

Tests inside a `:def` function:
```vim
vim9script
def Foo(): string
    return 'working'
enddef
def Func()
    echo 'Foo'->string()->eval()()
enddef
Func()
```
    E117: Unknown function: [unknown]
```vim
vim9script
def Foo(): string
    return 'working'
enddef
def Func()
    echo Foo->string()->eval()()
enddef
Func()
```
    working
```vim
vim9script
def MyFilter(i: number, v: string): bool
    return v =~ 'keep'
enddef
def Func()
    echo ['removeme', 'keepme', 'deleteme']->filter('MyFilter')
enddef
Func()
```
    ['removeme', 'keepme', 'deleteme']
```vim
vim9script
def MyFilter(i: number, v: string): bool
    return v =~ 'keep'
enddef
def Func()
    echo ['removeme', 'keepme', 'deleteme']->filter(MyFilter)
enddef
Func()
```
    ['keepme']
```vim
vim9script
def MyMap(i: number, v: number): number
    return v * 100
enddef
def Func()
    echo [1, 2, 3]->map('MyMap')
enddef
Func()
```
    [function('<80><fd>R1_MyMap'), function('<80><fd>R1_MyMap'), function('<80><fd>R1_MyMap')]
```vim
vim9script
def MyMap(i: number, v: number): number
    return v * 100
enddef
def Func()
    echo [1, 2, 3]->map(MyMap)
enddef
Func()
```
    [100, 200, 300]
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
def MySkip(): bool
    return synstack('.', col('.'))
        \ ->map({_, v -> synIDattr(v, 'name')})
        \ ->match('\ccomment') != -1
enddef
def Func()
    echo search('\<endif\>', '', 'MySkip')
enddef
Func()
```
    E1030: Using a String as a Number
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
def MySkip(): bool
    return synstack('.', col('.'))
        \ ->map({_, v -> synIDattr(v, 'name')})
        \ ->match('\ccomment') != -1
enddef
def Func()
    echo search('\<endif\>', '', MySkip)
enddef
Func()
```
    E703: Using a Funcref as a Number
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
def MySkip(): bool
    return synstack('.', col('.'))
        \ ->map({_, v -> synIDattr(v, 'name')})
        \ ->match('\ccomment') != -1
enddef
def Func()
    echo searchpair('\<if\>', '', '\<endif\>', '', 'MySkip')
enddef
Func()
```
    E703: Using a Funcref as a Number
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
def MySkip(): bool
    return synstack('.', col('.'))
        \ ->map({_, v -> synIDattr(v, 'name')})
        \ ->match('\ccomment') != -1
enddef
def Func()
    echo searchpair('\<if\>', '', '\<endif\>', '', MySkip)
enddef
Func()
```
    3
```vim
vim9script
def MyRep(): string
    return '1'
enddef
def Func()
    echo substitute('aaa', '.', 'MyRep', 'g')
enddef
Func()
```
    MyRepMyRepMyRep
    ✘
```vim
vim9script
def MyRep(): string
    return '1'
enddef
def Func()
    echo substitute('aaa', '.', MyRep, 'g')
enddef
Func()
```
    111
    ✔

---

Tests at script level:
```vim
vim9script
def Foo(): string
    return 'working'
enddef
echo 'Foo'->string()->eval()()
```
    E15: Invalid expression: )
```vim
vim9script
def Foo(): string
    return 'working'
enddef
echo Foo->string()->eval()()
```
    working
```vim
vim9script
def MyFilter(i: number, v: string): bool
    return v =~ 'keep'
enddef
echo ['removeme', 'keepme', 'deleteme']->filter('MyFilter')
```
    ['removeme', 'keepme', 'deleteme']
```vim
vim9script
def MyFilter(i: number, v: string): bool
    return v =~ 'keep'
enddef
echo ['removeme', 'keepme', 'deleteme']->filter(MyFilter)
```
    ['keepme']
```vim
vim9script
def MyMap(i: number, v: number): number
    return v * 100
enddef
echo [1, 2, 3]->map('MyMap')
```
    [function('<80><fd>R1_MyMap'), function('<80><fd>R1_MyMap'), function('<80><fd>R1_MyMap')]
```vim
vim9script
def MyMap(i: number, v: number): number
    return v * 100
enddef
echo [1, 2, 3]->map(MyMap)
```
    [100, 200, 300]
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
def MySkip(): bool
    return synstack('.', col('.'))
        \ ->map({_, v -> synIDattr(v, 'name')})
        \ ->match('\ccomment') != -1
enddef
echo search('\<endif\>', '', 'MySkip')
```
    E1030: Using a String as a Number
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
def MySkip(): bool
    return synstack('.', col('.'))
        \ ->map({_, v -> synIDattr(v, 'name')})
        \ ->match('\ccomment') != -1
enddef
echo search('\<endif\>', '', MySkip)
```
    E703: Using a Funcref as a Number
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
def MySkip(): bool
    return synstack('.', col('.'))
        \ ->map({_, v -> synIDattr(v, 'name')})
        \ ->match('\ccomment') != -1
enddef
echo searchpair('\<if\>', '', '\<endif\>', '', 'MySkip')
```
    E703: Using a Funcref as a Number
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
def MySkip(): bool
    return synstack('.', col('.'))
        \ ->map({_, v -> synIDattr(v, 'name')})
        \ ->match('\ccomment') != -1
enddef
echo searchpair('\<if\>', '', '\<endif\>', '', MySkip)
```
    3
```vim
vim9script
def MyRep(): string
    return '1'
enddef
echo substitute('aaa', '.', 'MyRep', 'g')
```
    MyRepMyRepMyRep
    ✘
```vim
vim9script
def MyRep(): string
    return '1'
enddef
echo substitute('aaa', '.', MyRep, 'g')
```
    111

---

Conclusions:

   - we can use a function name instead of a funcref, but only *without* quotes
   - for `search()`, we can't use a function name instead of a funcref (inconsistent)

To be consistent with `call()`, `setqflist()` and `timer_start()`:

   - we should be able to use a function name instead of a funcref *also* with quotes
   - for `search()`, we should be able to use a function name instead of a funcref

## ?

What about  builtin functions?   Can they  be used whenever  a function  name is
expected?

Tests inside a `:def` function:
```vim
vim9script
def Func()
    echo 'reltime'->string()->eval()()
enddef
Func()
```
    E117: Unknown function: [unknown]
```vim
vim9script
def Func()
    echo reltime->string()->eval()()
enddef
Func()
```
    E1001: variable not found: reltime
```vim
vim9script
def Func()
    echo ['removeme', 'keepme', 'deleteme']->filter('reltime')
enddef
Func()
```
    E121: Undefined variable: reltime
```vim
vim9script
def Func()
    echo ['removeme', 'keepme', 'deleteme']->filter(reltime)
enddef
Func()
```
    E1001: variable not found: reltime
```vim
vim9script
def Func()
    echo [1, 2, 3]->map('reltime')
enddef
Func()
```
    E121: Undefined variable: reltime
```vim
vim9script
def Func()
    echo [1, 2, 3]->map(reltime)
enddef
Func()
```
    E1001: variable not found: reltime
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
def Func()
    echo search('\<endif\>', '', 'reltime')
enddef
Func()
```
    E1030: Using a String as a Number
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
def Func()
    echo search('\<endif\>', '', reltime)
enddef
Func()
```
    E1001: variable not found: reltime
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
def Func()
    echo searchpair('\<if\>', '', '\<endif\>', '', 'reltime')
enddef
Func()
```
    E121: Undefined variable: reltime
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
def Func()
    echo searchpair('\<if\>', '', '\<endif\>', '', reltime)
enddef
Func()
```
    E1001: variable not found: reltime
```vim
vim9script
def Func()
    echo substitute('aaa', '.', 'reltime', 'g')
enddef
Func()
```
    reltimereltimereltime
    ✘
```vim
vim9script
def Func()
    echo substitute('aaa', '.', reltime, 'g')
enddef
Func()
```
    E1001: variable not found: reltime

---

Tests at script level:
```vim
vim9script
echo 'reltime'->string()->eval()()
```
    E15: Invalid expression: )
```vim
vim9script
echo reltime->string()->eval()()
```
    E121: Undefined variable: reltime
```vim
vim9script
echo ['removeme', 'keepme', 'deleteme']->filter('reltime')
```
    E121: Undefined variable: reltime
```vim
vim9script
echo ['removeme', 'keepme', 'deleteme']->filter(reltime)
```
    E121: Undefined variable: reltime
```vim
vim9script
echo [1, 2, 3]->map('reltime')
```
    E121: Undefined variable: reltime
```vim
vim9script
echo [1, 2, 3]->map(reltime)
```
    E121: Undefined variable: reltime
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
echo search('\<endif\>', '', 'reltime')
```
    E1030: Using a String as a Number
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
echo search('\<endif\>', '', reltime)
```
    E121: Undefined variable: reltime
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
echo searchpair('\<if\>', '', '\<endif\>', '', 'reltime')
```
    E121: Undefined variable: reltime
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
echo searchpair('\<if\>', '', '\<endif\>', '', reltime)
```
    E121: Undefined variable: reltime
```vim
vim9script
echo substitute('aaa', '.', 'reltime', 'g')
```
    reltimereltimereltime
    ✘
```vim
vim9script
echo substitute('aaa', '.', reltime, 'g')
```
    E121: Undefined variable: reltime

---

Conclusion:  Nothing works.

##
## ?
```vim
vim9script
def Func()
    let s:d = 123
enddef
defcompile
```
    E1101: Cannot declare a script variable in a function: s:d
```vim
vim9script
def Func()
    s:d = 123
enddef
defcompile
```
    E1089: unknown variable: s:d

Why can we define a variable with any scope in a `:def` function, *except* with the scope `s:`?
Is this documented?

Update: Yes, it's documented at `:h :def`:

   > If the script the function is defined in is Vim9 script, then script-local
   > variables can be accessed without the "s:" prefix.  **They must be defined**
   > **before the function is compiled.**

This behavior was introduced in 8.2.1320.
But  the commit  message does  not  seem to  have  the goal  of disallowing  the
definition of a  script-local variable in a `:def` function.   Does this suggest
it's a regression?

When was the quoted sentence in bold added to the help?
Before or after 8.2.1320?
If it was before, then it could be a regression.
Update: I think this paragraph was added in 8.2.0294.

Update: Actually, this behavior was not introduced in 8.2.1320.
On 8.2.1319, an error was already raised; although a different one:

    E1054: Variable already declared in the script: s:var

This error was raised starting from 8.2.0285.

---

I don't think it's a bug.  But you should document it in our notes.

## Vim9: cannot use the s: namespace in a :def function

**Describe the bug**

In Vim9 script, we cannot use the `s:` namespace in a `:def` function.

**To Reproduce**

Run this shell command:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            echo s:
        enddef
        defcompile
    EOF
    )

`E1075` is raised:

    E1075: Namespace not supported: s:

**Expected behavior**

**Environment**

 - Vim version: 8.2 Included patches: 1-1462
 - OS: Ubuntu 16.04.7 LTS
 - Terminal: XTerm(358)

**Additional context**

This issue is similar to https://github.com/vim/vim/issues/6480 , which was about the `g:` namespace, and was fixed in [8.2.1250](https://github.com/vim/vim/commit/2f8ce0ae8a8247563be0a77a308130e767e0566e).

---

The issue disappears at the script level:
```vim
vim9script
echo s:
```
    {}

---

`E1075` is not documented in the help, but it is also raised when we try to nest a script-local function inside another one:
```vim
vim9script
def Outer()
    def s:Inner()
    enddef
enddef
Outer()
```
    E1075: Namespace not supported: s:Inner()

However, in the first example, I'm not trying to define a nested script-local function.  I'm not even trying to define a script-local variable.

---

Unfortunately, I think it's working as intended.
This particular issue was briefly mentioned in #6480, but not fixed.
And I don't think it was forgotten, because the fix for that issue did take into consideration the `s:` namespace.
But it simply changed the error message from:

    E1050: Item not found: [empty]

To:

    E1075: Namespace not supported: s:

Maybe ask on #6480 why `s:` is not supported.
It would help if it was supported:

   - to refactor vim-search (see comment at the top of the autoload script)
   - to refactor future Vim script legacy functions where we've written `get(s:, ...)`
     (we have a few dozens of those)

If it can't be made to work, maybe this limitation should be documented (`:h vim9-gotchas`).

---

It might be documented at `:h :def`:

   > If the script the function is defined in is Vim9 script, then script-local
   > variables can be accessed without the "s:" prefix.  **They must be defined**
   > **before the function is compiled.**

But there's nothing  in there which says that we  cannot access the script-local
dictionary.

##
## ?
```vim
vim9script
let s:d = {'key': 0}
let s:d.key = 123
```
    ✔
```vim
vim9script
let s:d = {'key': 0}
def Func()
    let s:d.key = 123
enddef
defcompile
```
    E1101: Cannot declare a script variable in a function: s:d

I'm not trying to declare a script variable; I'm trying to add a key in a dictionary.
The error message is misleading.  Bug?
```vim
vim9script
let s:d = {'key': 0}
def Func()
    s:d.key = 123
enddef
defcompile
```
    Not supported yet: s:d.key = 123

To document: cannot use `d.key` in a `:def` function.

## ?

Add a comment here asking for line continuation to work for `->` too in an autocmd and in a custom Ex command?

<https://github.com/vim/vim/issues/6702>

---

What about mappings?
Contrary to what I said in the OP, I *think* it could work too.
They cannot use the Vim9 syntax at *execution* time, but I think they could at *install* time:

    nno <F3> :call A()
      \ <bar> call B()
      \ <bar> call C()<cr>

    →

    nno <F3> :call A()
        <bar> call B()
        <bar> call C()<cr>

I think line continuations are one of the most frustrating parts of legacy Vim script.  It might look like a detail, but I think it's important to eliminate them as much as possible in Vim9 script.  It makes the code much easier to read, write and maintain.

I think there are various ways to write a bar in the rhs of a mapping, and they can vary depending on how `'cpoptions'` is set; luckily, in a Vim9 script, the option is automatically reset to its default value.  So, only `<bar>` and `\|` can be used.

When parsing a mapping command, could Vim look for `<bar>` at the start of the next line, and if it's found, append it to the current line?

---

Maybe we  should ask for  another enhancement:  make mappings replace  `s:` with
`<SID>` automatically..

---

This excerpt from `:h <SID>` looks wrong:

   > When defining a function in a script, "s:" can be prepended to the name to
   > make it local to the script.  But when a mapping is executed from outside of
   > the script, it doesn't know in which script the function was defined.  To
   > avoid this problem, use "<SID>" instead of "s:".  The same translation is done
   > as for mappings.  This makes it possible to define a call to the function in
   > a mapping.

It seems that it  says that you need to prepent a function  name with `<SID>` if
you want to call it from a mapping.  That's not true.  Was it true in the past?

---

Mappings are really weird for a beginner.  Are there other enhancements we could
ask to make their definition more intuitive?

## ?
```vim
vim9script
def A()
    B()
    echom 'still running'
enddef
fu B()
    eval [][0]
endfu
A()
```
    E684: list index out of range: 0

`still running` was not executed, which seems correct.  Now, watch this:
```vim
vim9script
fu A() abort
    call s:B()
    echom 'still running'
endfu
fu B()
    eval [][0]
endfu
A()
```
    E684: list index out of range: 0
    still running

This time,  `still running` *was* executed,  even though `B()` raised  an error.
You  can fix  the issue  by defining  `B()` with  abort, but  why the  different
behavior?  Should it be  fixed?  Maybe it's a bug which  cannot be fixed because
of backwards compatibility.

##
## bug: imported constants and variables not added to the "s:" dictionary

    imported constant
```vim
vim9script
g:lines =<< trim END
    vim9script
    export const s:MYCONST = 123
END
mkdir('/tmp/import', 'p')
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

## ?

Vim9: the scope of an autoload variable is confusing

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        let foo#bar = 123
        echo g:
        echo s:
    EOF
    )

    {}
    {'foo#bar': 123}

This suggests that without an explicit prefix, an autoload variable is local to the script.
But watch this:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        s:foo#bar = 123
    EOF
    )

    E461: Illegal variable name: s:foo#bar

This suggests that an autoload variable *cannot* be script-local.
Either an autoload variable is script-local by default, and the second snippet should not raise an error, or it is *not* script-local by default and in the first snippet `s:` should *not* include a `foo#bar` key.

---

[We can omit the `g:` prefix](https://github.com/vim/vim/issues/6553) in front of the name of an autoload function in its header, and at any call site.

But we *cannot* omit `g:` for an autoload variable:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        let foo#bar = 123
    EOF
    )

    :echo foo#bar
    E121: Undefined variable: foo#bar

    :echo g:foo#bar
    E121: Undefined variable: g:foo#bar

Notice how an error is raised because `g:` is missing in the assignment.

To be consistent, I think one of these statements should be true:

   1. `g:` is enforced for autoload functions
   2. `g:` is disallowed for autoload functions
   3. `g:` is allowed for autoload variables

If `1.` is chosen, we need to write `g:` all the time:

   - when defining an autoload function
   - when calling an autoload function
   - when assigning a value to an autoload variable
   - when evaluating an autoload variable

If `2.` is chosen, we never need to write `g:`, but the help at `:h autoload` should be updated.
If `3.` is chosen, it never matters whether we write `g:` or omit it, but – again – the help at `:h autoload` should be updated.

FWIW, I would prefer `3.`, because it's more consistent with legacy Vim script.

---

   > Normally, in Vim9 script all functions are local.
   > To use a function outside of the script, it either has to be exported/imported, or made global.
   > Autoload scripts are different; they define a third type of function: "autoloadable".
   > Those are recognized by the "name#" prefix.
   > It's like these are exported to this autoload namespace.
   > These functions are not global, in the sense that the g: prefix is not used,
   > neither where it's defined nor where it is called.

Source: <https://github.com/vim/vim/issues/6553#issuecomment-665878820>

I think this suggests that autoload functions are automatically exported to some
autoload  namespace, and  can  be  used without  being  imported (maybe  they're
automatically imported when called).

Is the same true about autoload variables?
If so, does it make our previous analyses wrong?

##
## ?
```vim
nno <expr> <c-b> Map()

def Map()
    A()
    return ''
enddef

def A()
    invalid
enddef

call feedkeys("\<C-b>")
```
    E476: Invalid command: invalid

Why doesn't Vim raise any error for the missing return type in `Map()`'s header?

    E1096: Returning a value in a function without a return type

Update:  I think that `E476` is raised at compile time, not at runtime.
And at compile time, `E1096` is also raised:
```vim
def Map()
    A()
    return ''
enddef

def A()
    invalid
enddef
defcompile
```
    E476: Invalid command: invalid
    E1096: Returning a value in a function without a return type

But why doesn't Vim raise `E1096` in the first snippet, at compile time?
It's not because of the `<expr>` argument:
```vim
vim9script

def Map()
    A()
    return ''
enddef

def A()
    invalid
enddef

defcompile
```
Update:  You assume that `E1096` should be raised.
What if it's the other way around?  Maybe, it should *not* be raised.
Maybe Vim should stop the compilation as soon as an error is raised.
```vim
vim9script

def Func()
    invalid
    return ''
enddef

 defcompile
```
    E476: Invalid command: invalid

In this simpler example, only `E476` is raised.

If that's the case, then you must find out why `E1096` is raised here:
```vim
def Map()
    A()
    return ''
enddef

def A()
    invalid
enddef
defcompile
```
Update:  Maybe you have 2 errors, because you have 2 functions.
If you refactor the code to get only 1 function, then you only get 1 error.
But if  that's the case, then  why do we get  only 1 error here,  even though we
have 2 functions:
```vim
vim9script

def Map()
    A()
    return ''
enddef

def A()
    invalid
enddef

Map()
```
## ?
```vim
vim9script

def Map()
    A()
    return ''
enddef

def A()
    invalid
enddef

defcompile
```
    E476: Invalid command: invalid
    E1096: Returning a value in a function without a return type
```vim
vim9script

def Map()
    B()
    return ''
enddef

def B()
    invalid
enddef

defcompile
```
    E476: Invalid command: invalid

Why isn't `E1096` raised in the second snippet?
The code is identical; the only difference is that `A()` has been renamed into `B()`.
Same results if you rename `Map()` into `Func()`.

## ?
```vim
vim9script

def Map()
    A()
    return ''
enddef

def A()
    invalid
enddef

defcompile
```
    E476: Invalid command: invalid
    E1096: Returning a value in a function without a return type
```vim
vim9script

def Map()
    invalid
    return ''
enddef

defcompile
```
    E476: Invalid command: invalid

Why is `E1096` raised in the first snippet, but not in the second one?

## ?
```vim
nno <expr> <c-b> Map()

def Map()
    A()
    B()
    return ''
enddef

def A()
    invalid
enddef

def B()
    echom 'still alive'
enddef

call feedkeys("\<C-b>")
```
Why doesn't Vim print `still alive` after we press Enter?

## ?

Look at this script:

    ~/.vim/plugged/vim-lg-lib/import/lg/math.vim

In the `Max()` function, look at this line:

    elseif copy(numbers)->map({_, v -> type(v)})->index(v:t_float) == -1

Temporarily refactor to introduce an error:

    elseif !copy(numbers)->map({_, v -> type(v)})->index(v:t_float) == -1
           ^
           ✘

Start Vim like this:

    $ vim +"pu=[1, 2, 3]" +'exe "norm! gg\<c-v>G"' +'norm -m'
    :mess
    Vim(let):E1072: Cannot compare bool with number~

This error message is useless: no script name, no function name, no line number, ...
It has  been caught  by a `catch`  clause in a  `try` conditional  in `Opfunc()`
which is exported in `vim-lg-lib`.

Now, press `coV`, and repeat the process.  The same error is raised:

    Vim(let):E1072: Cannot compare bool with number

It looks  like there is still  not enough info,  but if you run  `:mess`, you'll
that we have a  whole stack trace.  Why was it not fully  printed when the error
was raised?

Now,  in  `~/.vim/plugged/vim-lg-lib/import/lg/math.vim`,  add  a  `:defcompile`
right after the `Min()` function, then run:

    $ vim +"pu=[1, 2, 3]" +'exe "norm! gg\<c-v>G"'
    " press:  -m
    Error detected while processing /home/user/.vim/plugged/vim-math/autoload/math.vim[10]../home/user/.vim/plugged/vim-lg-lib/import/lg/math.vim[51]..function <SNR>165_Max:~
    line    9:~
    E1072: Cannot compare bool with number~

That's much better.  But why do we need `:defcompile` to get more info here?
*Update:  `coV` would have had the same effect*

Try to fix all those issues, and try to find a method to quickly find the origin
of an error.   I'm tired of seeing  Vim9 errors and having to  find their origin
manually.  We should be  able to press `!w` and get the error(s)  in a qfl, just
like we could in Vim legacy.

##
## inconsistency: when we ask for the definition of a Vim9 function, comments are sometimes included, but not always.

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

`:vim9script` filters out whole commented lines in definitions of `:def` functions.
Same thing for empty lines.

Is it intended?
If so, should it be documented at `:h vim9`?

---

Note that this doesn't cause any  issue for our vim-stacktrace plugin because it
doesn't need  the *definition* of  a buggy function;  the plugin just  needs the
name of the script  where it's defined.  In fact, even if  the plugin needed the
definition, it couldn't have  it, because in Vim9 script, as  soon as a function
raises an error, its body is emptied.

## ?
```vim
vim9script
def Func()
    echo range(9)->map({_, v->v + 1})
enddef
Func()
```
    no error

Should we enforce proper use of whitespace around the `->` inside a lambda?

    echo range(9)->map({_, v->v + 1})
                           ^--^
                            ✘

    echo range(9)->map({_, v - >v + 1})
                           ^----^
                             ✔

## ?

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

## ?

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

## ?

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

This  error  is  annoying.   It  prevents  us  from  refactoring  the  start  of
the  autoload script  in  `vim-search`;  it also  prevents  us from  eliminating
`strpart()` in `ccomplete.vim`.

It may be a known limitation, listed at `:h todo`:

   > - Assignment to dict doesn't work:
   >       let ret: dict<string> = #{}
   >       ret[i] = string(i)

## ?

By default, a function is local to the current script, right?

Does that remain true for:

   - `function('Func')`
   - `:breakadd func Func`
   - `:prof func Func`
   ...

If not, is this a bug?

## Vim9: name of `:def` function can't start with a lowercase alphabetic character

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

---

Update: Wait.  That  would open the possibility  of a clash between  one of your
custom function and a builtin one.

Indeed, suppose that:

   - you name your function `len`
   - you call `len()` at the script level
   - there is no `len()` function in the script-local namespace, nor in the imported functions

Vim will probably look for your function in the global namespace.
If a custom `len()` is allowed, it will shadow the builtin `len()`.

I think  that what prevents  what you had  in mind is  the fact that  a function
without a `s:` prefix is not necessarily script-local; it can be global.

## Vim9: should Vim's help include its own Vim9 script style guide similar to ":h coding-style"?

Maybe it could be based on the one provided by Google.

## ?

Should we enforce the usage of full names of commands and options?

Would this make it easier for Vim developers to write new Vim9 features, and fix Vim9 bugs?

Would it provide other technical benefits?  Like maybe this would make it easier to write a [Vim9 parser](https://github.com/vim/vim/issues/6372), which in turn could be used to write other tools for Vim9, like a [full optimizer](https://github.com/vim/vim/issues/6372#issuecomment-652634882)?

---

FWIW, the Vimscript [style guide from Google](https://google.github.io/styleguide/vimscriptfull.xml?showone=Settings#Settings) recommends using full names:

   > Prefer long names of built in settings (i.e. tabstop over ts).

---

This would also have the obvious benefits of making people write code which is both more readable, and more consistent.  For example, there would be only a single way to execute `:nnoremap`, compared to 6 right now:

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

## ?
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

## ?

Those errors are present in the Vim9 tests, but are not documented:

`:h E451`
`:h E654`

`:h E1001`
`:h E1002`
`:h E1003`
`:h E1004`
`:h E1006`
`:h E1007`
`:h E1008`
`:h E1009`
`:h E1010`
`:h E1011`
`:h E1013`
`:h E1014`
`:h E1015`
`:h E1016`
`:h E1017`
`:h E1018`
`:h E1019`
`:h E1020`
`:h E1021`
`:h E1022`
`:h E1023`
`:h E1025`
`:h E1026`
`:h E1027`
`:h E1029`
`:h E1030`
`:h E1031`
`:h E1032`
`:h E1033`
`:h E1034`
`:h E1035`
`:h E1036`
`:h E1039`
`:h E1040`
`:h E1041`
`:h E1043`
`:h E1045`
`:h E1046`
`:h E1048`
`:h E1049`
`:h E1052`
`:h E1053`
`:h E1054`
`:h E1055`
`:h E1056`
`:h E1057`
`:h E1059`
`:h E1060`
`:h E1061`
`:h E1062`
`:h E1066`
`:h E1067`
`:h E1068`
`:h E1069`
`:h E1070`
`:h E1071`
`:h E1072`
`:h E1073`
`:h E1074`
`:h E1075`
`:h E1077`
`:h E1081`
`:h E1084`
`:h E1085`
`:h E1086`
`:h E1090`
`:h E1093`
`:h E1095`
`:h E1096`
`:h E1097`
`:h E1100`
`:h E1101`
`:h E1103`

---

Those errors are present in our Vim9 notes and in this file, but are not documented:

`:h E1001`
`:h E1013`
`:h E1016`
`:h E1017`
`:h E1041`
`:h E1044`
`:h E1048`
`:h E1051`
`:h E1066`
`:h E1073`
`:h E1075`
`:h E1077`
`:h E1081`
`:h E1084`
`:h E1086`
`:h E1088`
`:h E1096`
`:h E1100`

## ?

We can omit `s:` when the function starts with an uppercase character:
```vim
vim9script
def Func()
enddef
Func()
```
But not when it starts with a lowercase character:
```vim
vim9script
def s:func()
enddef
func()
```
    E117: Unknown function: func

Is it working as intended?  Should it be documented at `:h vim9-gotchas`?

Same thing with imported functions.

---

I think that's the  reason why you should always name your  def functions with a
name starting with a lowercase character.

## ?

A builtin function can shadow a script-local one:
```vim
vim9script
def s:len(): number
    return 123
enddef
echo len('abc')
```
Should Vim raise  an error when we  try to define a function  whose name clashes
with a builtin one?  I don't think so, because we can already define a `s:len()`
function in legacy...

## ?
```vim
vim9script
def FuncA(n)
    if n == 123
        FuncB(123)
    endif
enddef
def FuncB(n: number)
    echo n
enddef
FuncA(123)
```
    Error detected while processing command line..script /proc/30492/fd/11:~
    line    2:~
    E1077: Missing argument type for n~
    line    3:~
    E121: Undefined variable: n~
    line    6:~
    E193: :enddef not inside a function~
    line   10:~
    E117: Unknown function: FuncA~

This is way too verbose.
Couldn't Vim just report the first error?

## ?

    $ vim -Nu NONE -S <(cat <<'EOF'
        let s = 3
        let line = 'abcdef'
        echo line[s:]
    EOF
    )

    E731: using Dictionary as a String

Not easy to understand the error.
First, it is not obvious that `s:` was parsed as a dictionary (the one containing all the script-local variables).
Second, it is unexpected to see the word `String` mentioned in the message; in a string slice, we typically use numbers, not strings, to index some bytes (legacy) or characters (Vim9).

This would be better:

    E1234: cannot use s: Dictionary as an index

Because this message suggests that `s:` was parsed as a dictionary.

I was thinking that maybe Vim could be smarter and parse `s:` differently depending on whether it's followed by a variable name or not, but I don't think that's possible:

    'foobar'[s:var]

In this example, does `s:var` stand for a slice of one byte indexed by the variable `s:var`?
Or does it stand for a slice of several bytes, from the one indexed by `s` to the one indexed by `var`?
Right now, Vim uses the first interpretation.
However, to avoid any kind of confusion, maybe Vim9 script should enforce white space around `:` in a slice?
Actually, no, that's a bad idea.  I think it would make Vim raise an error when we use a script-local variable as a byte index.  The issue is that `:` is used both as a delimiter between indexes in a slice, *and* inside a scope.

---
```vim
let l = 3
let line = 'abcdef'
echo line[l:]
```
    E121: Undefined variable: l:

This is expected.  And the reason why the error message is different, is because
the code is not run inside a function; so there is no `l:` dictionary.

##
## documentation
### 61

You can't use `.` for concatenation.

You must use `..`:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        let str = 'a' . 'b'
    EOF
    )

    E15: Invalid expression: 'a' . 'b'

This is not documented at `:h vim9-differences`.

Although, there is this somewhere in the middle of the help:

   > When using `..` for string concatenation the arguments are always converted to
   > string. >
   >         'hello ' .. 123  == 'hello 123'
   >         'hello ' .. v:true  == 'hello true'

But this makes it seem as if `.` was still ok.
It is not.

I would write this instead:

   > `.` can no longer be used for string concatenation.  Instead, `..` must be used.
   > Note that `..` always converts its operands to string. >
   >         'hello ' .. 123  == 'hello 123'
   >         'hello ' .. v:true  == 'hello true'

### 99

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

### 103

   > The argument types and return type need to be specified.  The "any" type can
   > be used; type checking will then be done at runtime, like with legacy
   > functions.

Should we try to be as specific as possible when declaring a type?
If so, why?
Does it improve the performance?
Or does it allow to spot errors earlier?

If it  improves the performance,  what about composite types:  is `dict<string>`
better than `dict<any>`?   IOW, does being specific at the  "subtype" level help
too?

If `any` can have a negative impact  on the function's performance, it should be
mentioned, so that users don't abuse the `any` type.

### 129

A nested function is not always local to the outer function

   > When using `:function` or `:def` to specify a new function inside a function,
   > the function is local to the function.

This should be rephrased like this:

   > When using `:function` or `:def` to define a nested function inside a `:def` function,
   > the nested function is local to the outer function.

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

### 130

   > It is not possible to define a script-local function inside a function.

It *is* possible to define a script-local function inside another function.
The sentence should be rephrased like this:

   > It is not possible to define a script-local function inside a `:def` function.

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

### 136

   > - Local to **the current scope and outer scopes** up to the function scope.

Not clear.
I would rather read "the current code block and outer code blocks".

Rationale: Coming from  legacy Vim script,  there is  no smaller scope  than the
function one.  The current sentence implies that there is one – which is true in
Vim9 script – without  specifying what it is.  It's explained  a little later at
`:h vim9-declaration`, but imo `:h vim9-scopes` should be understandable on its own.

### 156

   > Variables can be local to a script, function or code block:

What about the other scopes?  buffer-local, window-local, ...
```vim
vim9script
b:var = 123
```
### 192

From `:h vim9-declaration /Global`:

   > Global, window, tab, buffer and Vim variables can only be used
   > without `:let`, because they are are not really declared, they can also be
   > deleted with `:unlet`.

There should be  a semicolon somewhere, but  I'm not sure which  comma should be
replaced.  Try this:

   > Global, window, tab, buffer and Vim variables can only be used
   > without `:let`**;** because they are are not really declared, they can also be
   > deleted with `:unlet`.

Or this:

   > Global, window, tab, buffer and Vim variables can only be used
   > without `:let`, because they are are not really declared**;** they can also be
   > deleted with `:unlet`.

---

Here is an explanation:

   > Somewhere along the way I realized that  allowing the user of :let with global
   > variables is inconsistent. It  would mean that script-local  variables need to
   > be declared with :let and then later  cannot be used with :let for assigning a
   > value,  while global  variables  would  allow :let  to  be  used anywhere.   I
   > consider it  simpler to only use  :let for declarations, and  global variables
   > are not really declared. I hope this works best.

Source: <https://github.com/vim/vim/issues/6514#issuecomment-662683671>

   > These  variables can  be set  to any  value in  legacy Vim  script and  legacy
   > functions. Specifying a type  has very limited use that way. It  would work to
   > catch mistakes in  Vim9 code, in case you  try to assign a value  of the wrong
   > type, but one  cannot assume that these variables actually  have the specified
   > type. This  also means  that in  compiled functions  the type  always must  be
   > checked anyway.  For consistency I thought it  might be better to just not use
   > types for  these variables, based  on the  namespace. It could be  possible to
   > attach the type to the variable  (would require more memory though). Thus then
   > what you get is  once a variable has been given a type  in Vim9 code, the type
   > will also be checked in legacy  code. This also has runtime overhead, the type
   > needs  to be  checked on  every  assignment. And then  you will  have some  g:
   > variables with a specified type and  some without. Also, what if a variable is
   > deleted and added back with a  different type? Would be confusing, and will be
   > hard to avoid.

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

### 196

   > Variables cannot shadow previously defined variables.

What does this mean?
Does it mean that you can't re-declare a variable?

Update:

Maybe  it means  that  we can't  have  2 variables  with the  same  name in  the
script-local namespace and the function-local (or block-local) one?
```vim
vim9script
let x = 123
def Func()
    let x = 456
enddef
defcompile
```
    E1054: Variable already declared in the script: x

Note  that  you *can*  have  2  variables with  the  same  name in  2  different
namespaces, like the global one and the function-local one:
```vim
vim9script
g:x = 123
def Func()
    let x = 456
enddef
defcompile
```
I guess that's because, in that case,  there is not really a shadowing; you need
to prefix the name of your global variable with `g:`.
So, when  you refer  to `x`,  there is  no ambiguity;  Vim has  to look  for the
variable in the function-local namespace.
In  contrast, in  the previous  snippet,  when you  refer  to `x`,  there is  an
ambiguity; Vim can look for the variable in 2 different namespaces.

Update: Ok.  Is your explanation still invalidated by these snippets?
```vim
vim9script
def g:Func()
    let Func = 0
enddef
defcompile
```
    E1073: name already defined: Func = 0
```vim
vim9script
def Func()
    g:Func = 0
enddef
defcompile
```
    ✔

In our Vim9 notes, we have a fold whose title is:

    cannot use the name of a function as a variable name

I think it's relevant.

### 208

We cannot declare a register inside a `:def` function.

Suggested patch:
```diff
diff --git a/runtime/doc/vim9.txt b/runtime/doc/vim9.txt
index 2c4d1dbc1..05456870d 100644
--- a/runtime/doc/vim9.txt
+++ b/runtime/doc/vim9.txt
@@ -206,6 +206,12 @@ at the script level. >
 Since "&opt = value" is now assigning a value to option "opt", ":&" cannot be
 used to repeat a `:substitute` command.

+							*E1066*
+It is not allowed to assign a value to a register with `:let`. >
+	let @a = 'my register'		# Error!
+	@a = 'my register'		# OK
+	setreg('a', 'my register')	# OK
+
 							*E1092*
 Declaring more than one variable at a time, using the unpack notation, is
 currently not supported: >
```
### 242

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

### 249

We can pass a function name to  functions which accept a funcref as an argument,
*without* quotes.

It's not documented.  There is this:

   > Omitting function() ~

   > A user defined function can be used as a function reference in an expression
   > without `function()`. The argument types and return type will then be checked.
   > The function must already have been defined. >

   >         let Funcref = MyFunction

   > When using `function()` the resulting type is "func", a function with any
   > number of arguments and any return type.  The function can be defined later.

But  it's about  the fact  that `function()`  *can* be  dropped, it  doesn't say
anything about the fact that the quotes *can* or *must* be dropped.  This should
be documented at `:h vim9-differences`.

<https://github.com/vim/vim/issues/6788>

### 304

From `:h E1050`:

   > recognized, it is required to put a colon before a range.  This will add
   > "start" and print: >

Why do  we have to  write a colon  before a range even  when it's preceded  by a
modifier like `:silent`?
```vim
vim9script
def Func()
    sil %d
enddef
Func()
```
    E1050: Colon required before a range
```vim
vim9script
def Func()
    :sil %d
enddef
Func()
```
    ✔

Shouldn't `:silent`  be enough to prevent  Vim from parsing/confusing `%`  as an
operator?

Maybe it's because modifiers have not been implemented yet.
<https://github.com/vim/vim/issues/6530#issuecomment-663903048>

### 350

   > No curly braces expansion ~

   > |curly-braces-names| cannot be used.

Something else cannot be used anymore in Vim9 script:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            exe 'let n = 123'
            echo n
        enddef
        Func()
    EOF
    )

    E1001: variable not found: n

I suspect it's working as intended, because this "assignment":

    exe 'let n = 123'

is similar to:

    let var = 'n'
    let {var} = 123

Example:

    $ vim -Nu NONE -S <(cat <<'EOF'
        let var = 'n'
        let {var} = 123
        echo n
    EOF
    )
    123~

Maybe the help should mention this pitfall, and *maybe* recommend a refactoring?

### 362

   > Comparators ~
   >
   > The 'ignorecase' option is not used for comparators that use strings.

The help  should say something about  whether a comparison operator  matches the
case or ignore the case by default; that is, what happens if you don't prefix it
with `#` nor `?`.

Answer: it matches the case.

### 367

Something should be said about the new rule which disallows white space:

   - before a comma separating 2 items in a list or dictionary
   - before a colon separating 2 items in a dictionary

And about the new rule which enforces white space after a colon separating a key
from its value in a dictionary.

### 420

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

### 438

At `:h  vim9-gotchas`, I would add  a gotcha about  the fact that you  can *not*
omit `s:` when calling a script-local or imported function from a `:fu` function.
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
    E117: Unknown function: Bar

The reason why  you may forget, is because  in Vim9 script you can  omit `s:` in
front of a function name most of the time; that is when:

   - defining a `:def` function
   - defining a `:fu` function
   - calling a script-local function from a `:def` function

---

Also, we can drop `:call` in commands and autocommands but not in mappings
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

Again,  it might  be considered  as  a pitfall  which would  benefit from  being
documented at `:h vim9-gotchas`.

Btw, the leading `<` is missing because it was parsed as the `:<` Ex command; as
a result, the rest of the line is parsed as an argument, but `:<` doesn't accept
this kind of argument (only a number).

---

Also, I would add something about `!`.
```vim
vim9script
def Func()
    # do sth
    return 123
enddef
!Func()
```
    zsh: parse error near `()'

    shell returned 1

I think it's a good decision that Vim still parses `!` as in legacy, because:

   - it's consistent and less unexpected for someone coming from legacy
   - you'll probably want to use `!` as the Ex command `:!` more often than as the `!` arithmetic operator

However, maybe it should be documented:

    !Func() # Error!
    eval !Func() # OK

### 463

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

### 518

We can nest `:def` inside `:fu`, but not the reverse.
```vim
vim9script
def Vim9()
    fu Legacy()
    endfu
enddef
Vim9()
```
    E1086: Cannot use :function inside :def

Suggested patch:
```diff
diff --git a/runtime/doc/eval.txt b/runtime/doc/eval.txt
index d8994ef00..4555603b8 100644
--- a/runtime/doc/eval.txt
+++ b/runtime/doc/eval.txt
@@ -11575,8 +11575,10 @@ See |:verbose-cmd| for more information.
 			NOTE: Use ! wisely.  If used without care it can cause
 			an existing function to be replaced unexpectedly,
 			which is hard to debug.
-			NOTE: In Vim9 script script-local functions cannot be
+			NOTE: In Vim9 script, script-local functions cannot be
 			deleted or redefined.
+			NOTE: In Vim9 script, `:function` can not be nested
+			inside `:def`.

 			For the {arguments} see |function-argument|.

diff --git a/runtime/doc/vim9.txt b/runtime/doc/vim9.txt
index 2c4d1dbc1..d11cf72a7 100644
--- a/runtime/doc/vim9.txt
+++ b/runtime/doc/vim9.txt
@@ -516,6 +516,9 @@ THIS IS STILL UNDER DEVELOPMENT - ANYTHING CAN BREAK - ANYTHING CAN CHANGE
 			script script-local functions cannot be deleted or
 			redefined later in the same script.

+							*E1086*
+			It is not allowed to nest `:function` inside `:def`.
+
 							*:enddef*
 :enddef			End of a function defined with `:def`. It should be on
 			a line by its own.
```
---

Trick to  memorize the  rules: we can  progress (legacy →  Vim9), but  we cannot
regress (Vim9 → legacy).

### 524

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

### 671

From `:h :vim9 /common`:

   > In Vim9 script the global "g:" namespace can still be used as before.  And the
   > "w:", "b:" and "t:" namespaces.  These have in common that variables are not
   > declared and they can be deleted.

Maybe environment variables should be mentioned as well.

And maybe registers (like `@r`).
Indeed, you can't use `:let` with them; but you can't you use `:unlet` either.

Also, I would rewrite the whole paragraph like this:

   > In Vim9 script the global "g:" namespace can still be used as before.  And the
   > "w:", "b:", "t:", and "$" namespaces.  These have in common that their
   > variables cannot be declared but can be deleted.
   > For variables which are local to a script, function or code block, the opposite
   > is true.  They can be declared but cannot be deleted.

### 730

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

    E1048: Item not found in script: BAR~

### 805

   > The error can be given at compile time, no error handling is needed at runtime.

If  the function  contains a  type error,  it's still  installed (like  a legacy
function), but its body is empty.

This is neat, and maybe it should be documented.
If a  legacy function  contains syntax/type errors,  and was  invoked frequently
(e.g. `InsertCharPre` autocmd),  the same  errors were raised  repeatedly.  This
shoud not happen with a `:def` function.

But note that this is limited to an error which is found at compile time; not at
execution time.

### 842

   > slower and means mistakes are found only later.  For example, when
   > encountering the "+" character and compiling this into a generic add
   > instruction, at **execution time** the instruction would have to inspect the type
   > of the arguments and decide what kind of addition to do.  And when the

The  help always  uses the  expression "runtime".   To be  consistent, "runtime"
should be used here too.

### 892

   > When sourcing a Vim9 script from a legacy script, only the items defined
   > globally can be used; not the exported items.

Actually, I think you can also use any item defined in the `b:`, `t:`, and `w:` namespace;
but not one defined in the `s:` namespace.

###
### `:h autoload`

`:h vim9` was correctly updated, but not `:h autoload`:
<https://github.com/vim/vim/issues/6553>

---

   > It's like these are exported to this autoload namespace.

If an autoload  function is really exported  to some namespace, does  it mean we
don't need to use the `export` command to export it?
And we  can automatically  import it  under whatever name  we want  from another
script?  Make some tests.

###
### concept of block-local function

There is this at `:h vim9-declaration`:

   > The variables are only visible in the block where they are defined and nested
   > blocks.  Once the block ends the variable is no longer accessible: >

But it's about variables; there is nothing about functions.

##
# Todo list
## some todo items are stale

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

### new batch of stale items

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

###
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
# Misc.
## highlighting
### `->`, `(`, `)` in `:echo` command

    $ vim -Nu NONE -S <(cat <<'EOF'
        let lines =<< trim END
            fu Func()
                echo substitute('aaa', 'b', 'c', '')->OtherFunc()
            endfu
        END
        call setline(1, lines)
        syn on
        set ft=vim
    EOF
    )

Wrong highlighting:

    echo substitute('aaa', 'b', 'c', '')->OtherFunc()
                                        ^^
                                        ✘

Can be fixed by allowing `vimOper` to be contained in the `vimEcho` region:

    syn region	vimEcho	... contains=vimFunc,vimFuncVar,vimString,vimVar,vimOper
                                                                         ^-----^

Other wrong highlighting:

    echo substitute('aaa', 'b', 'c', '')->OtherFunc()
                   ^                   ^
                   ✘                   ✘

Can be fixed by allowing `vimOperParen` to be contained in the `vimEcho` region:

    syn region	vimEcho	... contains=vimFunc,vimFuncVar,vimString,vimVar,vimOperParen
                                                                         ^----------^

### ?

In the "rhs" of a custom command, and of an autocmd, `call` is highlighted as a function
even when used as an Ex command.

### ?

In this snippet:

    def A()
        B(s)
    enddef

`(s` is wrongly highlighted with `vimSubst`.

    B(s)
     ^^
     ✘

### ?

Some highlighting is wrong inside a block.

    vim9script
    {
        let x = 123
    }

### ?

    do <nomodeline> QuickFixCmdPost copen
                    ^-------------^
                    not highlighted

### ?

    let x: list<dict<any>>
           ^-------------^
           not correctly highlighted

### ?

    vim9script
    let winid = 1
        ? getloclist(0, {'winid': 0}).winid
        : getqflist({'winid': 0}).winid

`getqflist()` is not highlighted as a function.
Dirty fix:

    syn clear vimCmdSep

Update: Actually, it's  correctly highlighted when  inside the body of  a custom
function.  How  does that  happen?  Understand  how could help  us fix  the next
issue.

---

The whole `getloclist()` line is wrongly highlighted.
Dirty fix:

    syn clear vimSearch

### ?

    do <nomodeline> ...
       ^----------^
            ✘

Also, look at this snippet:

    au VimEnter * if exists('#User#MyFlags')
        \ |     do <nomodeline> User MyFlags
        \ |     call s:build_flags()
        \ | endif

Here `<nomodeline>` is highlighted with `vimOption`.

##
## The descriptions of the local plugins are not aligned in the main help file:

    vim -Nu NORC -S <(cat <<'EOF'
        set rtp-=~/.vim
        set rtp-=~/.vim/after
        set rtp^=~/.vim/plugged/asyncmake
        set rtp^=~/.vim/plugged/vim-autoread
        set rtp^=~/.vim
        set rtp+=~/.vim/after
    EOF
    )

## duplicate runtime bugs

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

## `no_mail_maps`

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

## try finish @andymass patch regarding "setreg()" so that it gets merged

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

Each line of the register is going to be put on some line of the buffer.  And the cursor has a column position.  Those 2 numbers *may* give a valid position in the buffer; one for each register line.  I think Vim adds trailing spaces if, and only if, that position is valid and there exists a character in the buffer *after* it.

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

## abbreviation sometimes unexpectedly expanded inside a word

**Describe the bug**

An abbreviation is sometimes unexpectedly expanded in the middle of a word.

**To Reproduce**

Run this shell command:

    $ vim -Nu NONE -S <(cat <<'EOF'
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

