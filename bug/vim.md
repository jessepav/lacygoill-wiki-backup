# matchit

<https://github.com/chrisbra/matchit/issues/19#issuecomment-1221467387>

# inconsistent handling of `test` and `[` when testing output of command
#### For bugs

   - Rule Id: SC2243
   - My shellcheck version: 0.8.0
   - [x] The rule's wiki page does not already cover this
   - [x] I tried on https://www.shellcheck.net/ and verified that this is still a problem on the latest commit

#### Here's a snippet or screenshot that shows the problem:
```sh
#!/bin/bash
if test "$(mycommand --myflags)"
then
  echo "True"
fi
```
#### Here's what shellcheck currently says:

No error is given.

#### Here's what I wanted or expected to see:

This error is given:

    In /tmp/sh.sh line 4:
    if test "$(mycommand --myflags)"
            ^----------------------^ SC2243 (style): Prefer explicit -n to check for output (or run command without [/[[ to check for success).

Rationale: If we replace `test` with `[`, an error is given:
```sh
#!/bin/bash
if [ "$(mycommand --myflags)" ]
then
  echo "True"
fi
```
And in bash, according to `$ help [`, `[` is a synonym for `test`.  If that's the case, I would expect `SC2243` to be given for both `test` and `[`; not just for `[`.

Update: Actually, on the online version of shellcheck, no error is given even if we use `[`.
Yet another regression?

---

Also, we found this issue with the following snippet:

    # an error is given ✔
    [ ! "$(pidof process)" ]

    # no error is given ✘
    test ! "$(pidof process)"

##
# vim-fuzzy

I suspect that invoking `map()` to turn source lines into dictionaries is costly.
But we only need to do that for 3 sources:

    ┌──────────┬─────────────────────┐
    │ sources  │ extra info needed   │
    ├──────────┼─────────────────────┤
    │ Commands │ trailing + location │
    ├──────────┼─────────────────────┤
    │ HelpTags │            location │
    ├──────────┼─────────────────────┤
    │ Mappings │ trailing + location │
    └──────────┴─────────────────────┘

Notice that those sources should be rather short.
From a few hundreds to – at most – 10 to 20 thousands (for help tags).
As a result, it should not be too costly to turn their lines into dictionaries.

OTOH,  for a  source like  `Files`,  which can  include millions  of lines,  the
process might  be too  costly (in  addition to  being useless;  we don't  need a
`trailing` key,  nor a `location`  key, when we fuzzy  search through a  list of
files).

Conclusion: One  way  to  optimize  our  code   would  be  to  turn  lines  into
dictionaries *only* when really necessary.

---

For sources which require a `trailing` and/or a `location` key, could we get rid
of those keys?

---

In the future, we might also have other sources:

    BCommits (git commits for the current buffer)
    BLines (lines in the current buffer)
    BTags (tags in the current buffer)
    Buffers (open buffers)
    Commits (git commits)
    GFiles (git files; `git ls-files`)
    GFiles? (git files; `git status`)
    Lines (lines in loaded buffers)
    Marks
    RecentExCommands
    RecentSearchCommands
    Registers
    Rg
    Snippets
    Tags (tags in the project)
    Unichar (unicode characters)
    Windows (open windows)

For which ones would we need a `trailing` key and/or a `location` one?

##
# PRs
## ?

The patch [8.2.4891](https://github.com/vim/vim/releases/tag/v8.2.4891) colorizes more highlight group at `:help highlight-groups`.

We keep using our own version of the script, because it seems better:

    ~/.vim/pack/mine/opt/help/autoload/help.vim
    /export def HighlightGroups()

Open a PR to share your version.

## ?

Open a PR to document colored underlines.

##
# Vim9
## ?

   > The error is given at runtime. It would help if it was given earlier; i.e. at compile time.

<https://github.com/vim/vim/issues/10735>

## ?
```vim
vim9script

def Map()
    A()
enddef

def A()
    invalid
enddef

defcompile
```
    E476: Invalid command: invalid
    E1191: Call to function that failed to compile: <SNR>1_A
```vim
vim9script

def Map()
    B()
enddef

def B()
    invalid
enddef

defcompile
```
    E476: Invalid command: invalid

Why isn't `E1191` given in the second snippet?
The code is identical; the only difference is that `A()` has been renamed into `B()`.
The issue disappears if you rename `Map()` into `Func()`.

##
## type checking
### Vim9: unexpected type error

**Steps to reproduce**

Run this shell command:

    vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        var lla: list<list<any>> = [[{k: true}], []]
        var lda: list<dict<any>> = lla[0]
        echo lla[0]->map((_, d: dict<any>) => d.k)
    EOF
    )

`E1012` is given:

    E1012: Type mismatch; expected dict<any> but got bool in map()

**Expected behavior**

No error is given, because `lla[0]` is `[{k: true}]` whose type is `list<dict<bool>>`.  Which means that its items have the type `dict<bool>`.  Which means that `map()` operates on data of type `dict<bool>`, and not on data of type `bool` contrary to what the error message says:

    E1012: Type mismatch; expected dict<any> but got bool in map()
                                                 ^------^

And `dict<bool>` satisfies the `dict<any>` requirement from the type specification in the lambda's arguments:

    echo lla[0]->map((_, d: dict<any>) => d.k)
                            ^-------^

Because `dict<bool>` is just a special case of `dict<any>`.

**Version of Vim**

8.2 Included patches: 1-4953

**Environment**

Operating system: Ubuntu 20.04.4 LTS
Terminal: xterm
Value of $TERM: xterm-256color
Shell: GNU bash, version 5.0.17

**Additional context**

The issue disappears if we remove the intermediate `lda` assignment:
```vim
vim9script
var lla: list<list<any>> = [[{k: true}], []]
echo lla[0]->map((_, d: dict<any>) => d.k)
```
    [true]

But why does this assignment matter?

---

As a workaround, we can make a `copy()`:
```vim
vim9script
var lla: list<list<any>> = [[{k: true}], []]
var lda: list<dict<any>> = lla[0]->copy()
echo lla[0]->map((_, d: dict<any>) => d.k)
```
    [true]

---

In the `lda` assignment, if we replace the subtype `any` with `bool`, a slightly different error is given:
```vim
vim9script
var lla: list<list<any>> = [[{k: true}], []]
var lda: list<dict<bool>> = lla[0]
echo lla[0]->map((_, d: dict<any>) => d.k)
```
    E1012: Type mismatch; expected dict<bool> but got bool in map()

Why does Vim expect `dict<bool>` in `map()`?  Shouldn't it expect `dict<any>`?

---

Simplied MRE:
```vim
vim9script
var l: list<any> = [{k: true}]
var x: list<dict<bool>> = l
echo l->map((_, d: dict<any>) => d.k)
```
    E1012: Type mismatch; expected dict<bool> but got bool in map()

Update: I think that's because assigning `l` to a variable causes Vim to update its type.  It goes from `list<any>` to `list<dict<bool>>`.  If that's the case, then the previous snippet is equivalent to:
```vim
vim9script
var l: list<dict<bool>> = [{k: true}]
echo l->map((_, d: dict<any>) => d.k)
```
    E1012: Type mismatch; expected dict<bool> but got bool in map()

### ?
```vim
vim9script
def Func()
    [0]->map((..._) => {
    })
enddef
Func()
```
    E1013: Argument 2: type mismatch, expected func(...): any but got func(...list<any>)

What's the issue here?  The types of  the lambda's arguments, or the missing one
for its return value?

And if the code is really wrong, why no error here:
```vim
vim9script
def Func()
    [0]->map((..._) => ({}))
enddef
Func()
```
    no error

Also, watch this:
```vim
vim9script
def Func()
    [0]->map((..._): any => {
        return 0
    })
enddef
Func()
```
    no error

This suggests that the issue was the missing return type.
But now, watch this:
```vim
vim9script
def Func()
    [0]->mapnew((..._) => {
    })
enddef
Func()
```
    no error

This time, no return type; and yet no error.
Why does `mapnew()` fixes the issue here?   It should only make a difference for
a variable with a declared type.  `[0]` is not a declared variable.

And here:
```vim
vim9script
def Func()
    [0]->map((_, _) => {
    })
enddef
Func()
```
    E1013: Argument 2: type mismatch, expected func(?number, ?any): any but got func(any, any)
                                                    ^        ^
Why are the expected arguments optional?

### ?
```vim
vim9script
def Func()
    var n: number = 1
    var s: string = n != 0 ? n : ''
enddef
defcompile
```
    no error

Should an error be given?  The snippet will give an error at runtime anyway.

---
```vim
vim9script
def Func()
    [{n: 123}]->map((_, d: dict<float>) => 0)
enddef
defcompile
```
    no error

<https://github.com/vim/vim/issues/9415#issuecomment-1001535428>
<https://github.com/vim/vim/issues/9802#issuecomment-1046244520>

The issue disappears when we get rid of `map()`:
```vim
vim9script
def Func()
    ((d: dict<float>) => 0)({n: 123})
enddef
defcompile
```
    E1013: Argument 1: type mismatch, expected dict<float> but got dict<number>

Also, this shows that the argument type is (sometimes?) checked at compile time,
but the return type never seems to be:
```vim
vim9script
def Func()
    ((d): dict<float> => d)({n: 123})
enddef
defcompile
```
    no error

<https://github.com/vim/vim/issues/9415#issuecomment-1001535428>

I think the last snippet is equivalent to this:
```vim
vim9script
def Foo(d: any): dict<float>
    return d
enddef
def Func()
    Foo({n: 123})
enddef
defcompile
```
    no error

Should Vim complain that the type of `d` (`any`) is not compatible with the return type?
Simplified MRE:
```vim
vim9script
def Func(): string
    var x: any
    return x
enddef
defcompile
```
    no error

<https://github.com/vim/vim/issues/9842#issuecomment-1049996566>

### ?
```vim
vim9script
var synstack: string = synstack('.', col('.'))
    ->mapnew((_, v: number): string => v->synIDattr('name'))
```
    E1012: Type mismatch; expected string but got list<unknown>
                                                       ^-----^
```vim
vim9script
def Func()
    var synstack: string = synstack('.', col('.'))
        ->mapnew((_, v: number): string => v->synIDattr('name'))
enddef
Func()
```
    E1012: Type mismatch; expected string but got list<any>
                                                       ^^^

Inconsistent?

Also, why not `list<string>`?
Can't Vim use the specified return type used in the lambda?

    ->mapnew((_, v: number): string => v->synIDattr('name'))
                             ^----^

###
### ?
```vim
vim9script
var InlineFunc = () => {
    return 123
}
echomsg InlineFunc->typename()
```
    func()
```vim
vim9script
def Func()
    var InlineFunc = () => {
        return 123
    }
    echomsg InlineFunc->typename()
enddef
Func()
```
    func(): number

Inconsistent.  The first snippet should output `func(): number`, just like the second one.

---
```vim
vim9script
def Foo()
    setlocal comment<
enddef
echo Foo->typename()
var Bar = () => {
    setlocal comment<
}
echo Bar->typename()
```
    func()
    func()
```vim
vim9script
function Foo()
    setlocal comment<
endfunction
echo Foo->typename()
legacy let g:Bar = {-> execute('setlocal comment<')}
echo g:Bar->typename()
```
    func(...): any
    func(...): unknown

Inconsistent?  Shouldn't it be:

    func(...): unknown
    func(...): unknown

### ?
```vim
vim9script
def Func()
    var s: list<string>
    s = [0]->map((_, v): number => '')
enddef
defcompile
```
    E1012: Type mismatch; expected number but got string

Is the error message easy enough to understand?

---

How about these ones?
```vim
vim9script
var d: dict<any> = {a: 0, b: ''}
    ->filter((_, v: string) => []->index('') >= 0)
```
    E1013: Argument 2: type mismatch, expected string but got number
```vim
vim9script
var d: dict<any> = {a: 0, b: ''}
    ->map((_, v: string) => []->index(''))
```
    E1013: Argument 2: type mismatch, expected string but got number

In both of them, the issue is in the 2nd argument of `filter()`/`map()`.
Not the 2nd argument of `index()`.
Not obvious.

### ?
```vim
vim9script
def Func(l: any)
    eval l[0] > 1 ? 2 : l[1]
enddef
Func(['', ''])
```
    E1030: Using a String as a Number: ""

Expected error, but the message could be better.
There are several operations going on here:

    eval l[0] > 1 ? 2 : l[1]
          ^^^ ^   ^   ^  ^^^

It might not be obvious which one expects a number instead of a string.
```vim
vim9script
def Func()
    eval '' > 1
enddef
Func()
```
    E1072: Cannot compare string with number

This message is better, because we immediately know that the issue comes from `>`.

Update: Actually, I suspect that we – in the general case – really need more context:

    E1234: Cannot compare string with number in: '' > 1

### ?

Check whether `typename()` returns a good signature for all builtin functions.

---
```vim
vim9script
echo 'len'->function()->typename()
```
    func([unknown]): number
         ^-------^
         wouldn't `any` be better?

##
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
issue; like: what does that function where an error was given?
Sure, you can use `:function` instead; but it's inconsistent to define a function with
`:def` then ask for its definition with `:function`.
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
    function s:def_complete(argLead, _l, _p) abort
        let argLead = substitute(a:argLead, '^\Cs:', '<SNR>[0-9]\\\\\\{1,}_', '')
        return getcompletion(argLead, 'function')->map('substitute(v:val, "($\\|()$", "", "")')
    endfunction
    function s:def(name) abort
        let name = trim(a:name, '()')
        try
            exe 'def ' .. name
        catch
            return 'echoerr ' .. string(v:exception)
        endtry
        return ''
    endfunction

##
## can delete a function-local or block-local function nested in a legacy function

MRE for a function-local function:

    $ vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        function Outer()
            def Inner()
                echo 'inner'
            enddef
            delfunction Inner
        endfunction
        Outer()
    EOF
    )

Actual: No error is given
Expected: E130 or E1084 is given (preferably the latter):

    E130: Unknown function: Inner
    E1084: Cannot delete Vim9 script function Inner

Rationale: to be consistent with script-local functions which can't be deleted.
```vim
vim9script
function Func()
endfunction
delfunction Func
```
    E1084: Cannot delete Vim9 script function Func
```vim
vim9script
def Func()
enddef
delfunction Func
```
    E1084: Cannot delete Vim9 script function Func

---

MRE for a block-local function:
```vim
vim9script
function Outer()
    if v:true
        def Inner()
            echo 'inner'
        enddef
        delfunction Inner
    endif
endfunction
Outer()
```
    no error

---

If this is working as intended, then the help should be updated at `:help vim9-scopes`.

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

## inconsistent error message when trying to delete local function nested in ":def" function

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

Note: the error is only given for a `:def` inside a `:def`.
If the outer function  is a `:function`, no error is given; no  matter the type of the
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

Note: the error is only given for a `:def` inside a `:def`.
If the outer function  is a `:function`, no error is given; no  matter the type of the
inner function.

---

No issue for an imported function:
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
set runtimepath+=/tmp
import 'foo.vim'
const Func = foo.Imported
delfunction Func
```
    E1084: Cannot delete Vim9 script function Func

This is consistent with:
```vim
vim9script
def Func()
enddef
delfunction s:Func
```
    E1084: Cannot delete Vim9 script function s:Imported

##
## Ideas to make Vim script less weird.
### Make all builtin functions immune to user settings

   - `byte2line()` depends on `'fileformat'`
   - `byteidxcomp()` depends on `'encoding'`
   - `char2nr()` depends on `'encoding'` (can be overridden by optional 2nd argument)

   - `cindent()` depends on `'cindent'` and `'tabstop'` (we don't want to change that, right?)
   - `indent()` depends on `'tabstop'` (idem)
   - `lispindent()` depends on `'lisp'`, `'tabstop'` (idem)

   - `col()` depends on `'virtualedit'`
   - `confirm()` depends on `'guioptions'`
   - `cursor()` depends on `'virtualedit'`
   - `executable()` depends on `'shell'`

   - `expand()` depends on `'wildignorecase'`, `'wildignore'` and `'suffixes'`
     (those last 2 can be overridden by optional 2nd argument)

   - `findfile()` depends on `'suffixesadd'`
   - `fnameescape()` depends on `'isfname'`
   - `garbagecollect()` depends on `'updatetime'`
   - `getcompletion()` depends on `'wildignorecase'`
   - `getpos()` depends on `'virtualedit'`

   - `glob()` depends on `'wildignorecase'`, `'wildignore'` and `'suffixes'`
     (those last 2 can be overridden by optional 2nd argument)

   - `globpath()` depends on `'wildignore'` and `'suffixes'` (not `'wildignorecase'`?)
   - `line2byte()` depends on `'fileformat'`, `'encoding'`
   - `list2str()` depends on `'encoding'` (can be overridden by 2 optional argument)
   - `match()` depends on `'ignorecase'`
   - `nr2char()` depends on `'encoding'`
   - `py3eval()` depends on `'encoding'`
   - `readfile()` depends on `'encoding'`

   - `search()` depends on `'ignorecase'`, `'smartcase'`, `'magic'`, `'cpo'`, `'wrapscan'`
     (the latter can be overridden by an optional flag; `'cpo'` is really BAD, right?)

   - `searchpair()` depends on `'ignorecase'`
   - `setpos()` depends on `'virtualedit'`
   - `shellescape()` depends on `'shellslash'` and `'shell'`

I've stopped looking at `shellescape()` ...
If you want to go on, look for this pattern:

    '[a-z]\{2,\}'

Remember that not all functions are documented at `:h eval`.
Some of them are in other pages; execute this to find the links:

    :g/functions.*documented/#

### Add more functions to reduce the need to ":execute" commands with dynamic arguments

   > Eval'ed   strings   run   in   unexpected  contexts   and   don't   go   through
   > parsing/expansion when you think it would.
   > And you cannot catch errors when the  script is parsed because you don't get the
   > AST until the very execution.  And let's not get into performance.

<https://www.reddit.com/r/vim/comments/54224o/why_is_there_so_much_hate_for_vimscript/d8135xm/>

---

This edits the file `myfile`:
```vim
vim9script
var myfile =  '/tmp/file'
edit myfile
```
If you want to edit `/tmp/file`, you need `:exe`:
```vim
vim9script
var myfile =  '/tmp/file'
exe 'edit ' .. myfile
```
But `:exe` has multiple drawbacks:

   - `:exe` prevents Vim from compiling the command,
     which in turn causes worse performance and no early type checking at compile time
   - `:exe` makes us lose syntax highlighting in the literal parts of the command
   - `:exe` might require to nest a quote inside a string, which can be tricky
   - `:exe` makes it difficult to determine what's literal and what's evaluated (and when it's evaluated)

There would be no such issue with a function:
```vim
vim9script
var myfile = '/tmp/file'
edit(myfile)
```
Also, a function  can be used as a  method which is nice to  read/write when the
first argument is obtained via another function or chain of functions.

Also, some  commands parse  a bar as  part of their  argument (e.g.  `:g`) which
often creates an ambiguity:

    g/pat/Cmd | OtherCmd
              ^
              will this bar terminate `:g` or `:Cmd`; only way to find out is to read :h :bar

With a function, no such ambiguity:

    global(lnum1, lnum2, 'pat', 'Cmd') | OtherCmd

Also, for some commands like `:au`,  `:com`, `:nno`, ... this would let us
remove  some undesirable  explicit continuation  lines  which we  need when  the
command  is  too  long to  fit  on  a  single  screen line  (which  does  happen
sometimes).

Also,  it would  make it  easier to  add new  arguments; like  one to  bind some
documentation  to mappings/commands/autocmds...  similar  to  the `-N`  argument
which can be  passed to the tmux  command `bind-key` which attaches a  note to a
newly installed key binding.
Relevant feature request: <https://github.com/vim/vim/issues/8039>

Also, it would  let us remove the  last few explicit continuation  lines that we
still need to write here and there:

    syn region xLinkText matchgroup=xLinkTextDelimiter
        \ start=/!\=\[\ze\_[^]]*] \=[[\x28]/ end=/\]\ze \=[[\x28]/
        \ nextgroup=xLink keepend concealends skipwhite

    →

    syntax('region', 'xLinkText', {
        matchgroup: 'xLinkTextDelimiter'
        start: '/!\=\[\ze\_[^]]*] \=[[\x28]/ end=/\]\ze \=[[\x28]/',
        nextgroup: 'xLink',
        keepend: true,
        concealends: true,
        skipwhite: true,
    })

Here are other real examples where we still have explicit continuation lines:

    au User MyFlags statusline#hoist('global',
        \ '%{&ve isnot# "' .. &ve .. '" && mode(1) is# "n" ? "[ve=" .. &ve .. "]" : ""}', 8,
        \ expand('<sfile>:p') .. ':' .. expand('<sflnum>'))

    com -bar -nargs=? -range=% -complete=custom,myfuncs#wfComplete
        \ WordFrequency
        \ myfuncs#wordFrequency(<line1>, <line2>, <q-args>)

    nno <expr> <cr> !empty(&buftype)
        \ ?     '<cr>'
        \ :     '<cmd>' .. getbufvar('%', 'cr_command', 'norm! 80<bar>') .. '<cr>'

With functions, we  could edit the statements as we  like; splitting and joining
lines wouldn't require any further edit (i.e. no backslash to remove or to add).

---

Try to get statistics on what are the most frequent Ex commands for which we need `:exe`.
Those would be good candidates for introducing equivalent functions.

Session files use a lot of `:exe` for `:resize`:

    exe '1resize ' .. ((&lines * 23 + 16) / 33)

And a few for `:bwipe` and `:source`:

    silent exe 'bwipe ' . s:wipebuf
    exe "source " . fnameescape(s:sx)

---

    \%(^\s*#\s.*\)\@<!\C\<exe\%[cute]\>(\@!

    868 matches in total

    b:undo_* = ?
    :set = ? (for keycodes which don't have matching option name)

    :norm = ?
    :hi = ?
    :syn = ? (match = ?, region = ?, keyword = ?, clear = ?, cluster = ?, include = ?, list = ?)

    :s = ?
    :g/v = ?

    :! = ?
    :[nx]no = ?
    :au = ?
    :[s]b = ?
    :bw = ?
    :cgetbuffer = ?
    :def = ?
    :do = ?
    :e = ?
    :j = ?
    :helptags = ?
    :m = ?
    :q = ?
    :r = ?
    :so = ?
    :sp = ?
    :tabe = ?
    :tabnew = ?
    :tabnext = ?
    :undo = ?
    :[l]vim = ?
    :vnew = ?
    :windo = ?
    :wundo = ?

### Autocmds

An augroup could clear itself automatically (especially useful for buffer-local autocmds):

    augroup my_group
        au!
        au Event * " do sth
    augroup END

    →

    augroup my_group
        au Event * " do sth
    augroup END

### Misc
#### provide a syntax to evaluate an expression and discard its value in an `<expr>` or `C-r =` mapping

Right now we need to use `[-1]` which looks weird.
Besides, it  doesn't work anymore in  Vim9 script when applied  to an expression
which evaluates to a number:
```vim
vim9script
def Func()
    feedkeys('q', 'in')[-1]
enddef
Func()
```
    E909: Cannot index a special variable

So, we'll have to use `? '': ''`, which looks cumbersome.

---

BTW, what is this "special variable" Vim is talking about?
And why is it not like at the script level?
```vim
vim9script
feedkeys('q', 'in')[-1]
```
    E1062: Cannot index a Number

#### Allow `'.'` as a shorthand for `col('.')` whenever a function argument expects a column number.

Allow `'.'` as a shorthand for  `line('.')` and `col('.')` regardless of whether
the function can work on other buffers.  For example, this doesn't work:

    call prop_type_add('number', {'highlight': 'Constant'})
    call prop_add('.', '.', {'length': 3, 'type': 'number'})
                  ^------^
                     ✘

That's because `prop_add()`  can work on inactive buffers, where  the concept of
"current" line or column doesn't make sense.
Still, it would be nice if it worked.

---

Look for which functions:

   - support `'.'` as a shorthand
   - don't support `'.'` as a shorthand, but would benefit from it
   - expect a `{row}` and/or `{col}` argument which describe *cells* positions

---

Unrelated, but usually, we  can use `'.'` as a shorthand  for `line('.')` in all
functions which can only work on the current buffer.
But I found 1 exception; the `{stopline}` argument in `search()` (and `searchpos()`):
```vim
eval repeat(['some text'], 2)->setline(1)
echo search('some', 'n', '.')
```
    2
    ✘
    should be 0
```vim
eval repeat(['some text'], 2)->setline(1)
echo search('some', 'n', line('.'))
```
    0
    ✔

#### Introduce syntax to reduce comment a regex more easily

Take inspiration from perl:

<https://perldoc.perl.org/perlfaq6#How-can-I-hope-to-use-regular-expressions-without-creating-illegible-and-unmaintainable-code%3f>

Add an `x` flag to:

    :g
    :lvimgrep
    :lvimgrepadd
    :match
    :s
    :sort
    :syn match
    :syn region
    :vimgrep
    :vimgrepadd
    matchadd()
    pattern used in range
    search()
    searchpair()
    searchpairpos()
    searchpos()

---

We could rewrite this:

    :s/<\%([^>'"]*\|\%(".*"\)\@>\|\%('.*'\)\@>\)\+>//g

Into this:

    :s/ <                    # opening angle bracket
         \%(                 # Non-backreffing grouping paren
             [^>'"] *        # 0 or more things that are neither > nor ' nor "
                 \|          #    or else
             \%(".*"\)\@>    # a section between double quotes (stingy match)
                 \|          #    or else
             \%('.*'\)\@>    # a section between single quotes (stingy match)
          \)\+               #   all occurring one or more times
          >                  # closing angle bracket
    //gx                     # replace with nothing, i.e. delete
       ^
       new flag which lets us comment a regex

But this requires a new feature: the ability to break a regex on multiple lines.
If this is made to work, it should be disallowed to omit the last delimiters.
Otherwise, there's ambiguity:

    :s/ <

Does the previous substitution removes a space followed by an opening angle bracket?
Or does it continue on the next line?

Also, we can't provide a flag to some commands like `:g`...

#### Introduce syntax to make functions self-documenting

Should we borrow this Python syntax?

    def Func():
        """
        some
        multiline
        docstring
        """
        some code

##
## Indentation related issues
### Vim9: "=" wrongly re-indents a dictionary returned from a function

**Describe the bug**

In Vim script, using `=` to re-indent a function returning a dictionary wrongly increases the indentation of its footer (i.e. `:enddef`).

**To Reproduce**

Run this shell command:

    $ vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        var lines =<< END
        def Func(): dict<any>
            return {
                a: 1,
                b: 2,
            }
        enddef
    END
        setline(1, lines)
        syntax on
        filetype indent on
        set ft=vim
        norm! gg=G
    EOF
    )

The buffer contains these lines:

    def Func(): dict<any>
            return {
                    a: 1,
                    b: 2,
                    }
            enddef

Notice that `:enddef` has a bigger indentation level than `:def`.

**Expected behavior**

`:enddef` has the same indentation level as `:def`.  Something like:

    def Func(): dict<any>
            return {
                    a: 1,
                    b: 2,
            }
    enddef

**Environment**

 - Vim version: 8.2 Included patches: 1-3270
 - OS: Ubuntu 20.04.2 LTS
 - Terminal: XTerm(353)

**Additional context**

Not sure it's correct, but in `$VIMRUNTIME/indent/vim.vim`, there is this block:

    " A line ending in "{" or "[" is most likely the start of a dict/list literal,
    " indent the next line more.  Not for a continuation line or {{{.
    if !ends_in_comment && prev_text_end =~ '\s[{[]\s*$' && !found_cont
      let ind = ind + shiftwidth()
    endif

Inside, include this `elseif`:

    elseif getline(v:lnum) =~ '^\s*[\]})]\+\s*$'
      let ind -= shiftwidth()

Update:  This breaks the fix for <https://github.com/vim/vim/issues/7798>

    $ vim -Nu <(tee <<'EOF'
        vim9script
        var lines =<< trim END
            vim9script
            def Func()
                for x in [
                    {key: 'value'},
                ]
                    eval 0
                endfor
            enddef
            Func()
        END
        lines->setline(1)
        set expandtab shiftwidth=4
        filetype plugin indent on
        set ft=vim
        silent normal! =G
    EOF
    )

### ?

    $ vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        packadd matchit
        filetype indent on
        var lines =<< trim END
            vim9script
            def Func()
              var d = dd
                ->extend({
              })
              eval 0
            enddef
        END
        lines->setline(1)
        set ft=vim
        norm! gg=G
    EOF
    )

Expected:

    vim9script
    def Func()
            var d = dd
            ->extend({
            })
            eval 0
    enddef

Actual:

    vim9script
    def Func()
            var d = dd
            ->extend({
            })
    eval 0
    enddef
    7 lines indented

###
### ?

    $ vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        var lines =<< trim END
            vim9script
            #     {
        END
        lines->setline(1)
        syntax on
        filetype plugin indent on
        set ft=vim
        feedkeys("Go\e")
    EOF
    )

Expected:

    vim9script
    #     {
    #

Actual:

    vim9script
    #     {
            #

---

    $ vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        var lines =<< trim END
            vim9script
            #     var d = {
            #     }
        END
        lines->setline(1)
        syntax on
        filetype plugin indent on
        set ft=vim
        syntax match xxxCommentxxx /#.*/
        feedkeys("GO\e")
    EOF
    )

Expected:

    vim9script
    #     var d = {
    #
    #     }

Actual:

    vim9script
    #     var d = {
            #
    #     }

---

    $ vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        var lines =<< trim END
            vim9script
            #     var d = {
            #         k: '
            #     }
        END
        lines->setline(1)
        syntax on
        filetype plugin indent on
        set ft=vim
        syntax match xxxCommentxxx /#.*/
        feedkeys("3GAend\e")
    EOF
    )

Expected:

    vim9script
    #     var d = {
    #         k: 'end
    #     }

Actual:

    vim9script
    #     var d = {
            #         k: 'end
    #     }

---

    $ vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        var lines =<< trim END
            vim9script
            #     var d = {
            #         k: [],
            #     }
        END
        lines->setline(1)
        syntax on
        filetype plugin indent on
        set ft=vim
        syntax match xxxCommentxxx /#.*/
        feedkeys("3Gf[a\r\e")
    EOF
    )

Expected:

    vim9script
    #     var d = {
    #         k: [
    #         ],
    #     }

Actual:

    vim9script
    #     var d = {
    #         k: [
            #         ],
    #     }

---

Update:  I think most of these issues come from here:

    let ends_in_comment = has('syntax_items')
          \ && synIDattr(synID(lnum, len(getline(lnum)), 1), "name") =~ '\(Comment\|String\)$'
                                                                                            ^

Inside  comments,  we  might  have  custom nested  groups  whose  names  contain
`Comment`, but not at the end.  For example, `vim9CommentCodeBlock`.

A possible fix would be to simply remove the anchor `$`.
Also, we might want to include `\c` in  the pattern to make it more resilient in
case the syntax plugin changes the case of the comment group name.
Also, we might want `synIDtrans()` (or not...).

### ?

Consider this script:

    vim9script

    var a = ''
        ->len()

    var b = ''

Press `O` from the `->len()` line: the cursor is on the first column.
Press `O` from the `var b` line: the cursor is on the `&sw`-th column.

It *seems* inconsistent.

### ?

    $ vim -Nu <(tee <<'EOF'
        vim9script
        set lines=24
        set nostartofline
        set rtp-=~/.vim rtp-=~/.vim/after
        nnoremap % <Cmd>call cursor(57, 1)<cr>
        filetype plugin indent on
        var lines = ['# {{{']
            + repeat(['#'], &lines)
            + ['def Func() #{{{']
            + ['    eval {0']
            + ['        0']
            + ['        0}']
            + ['    return 0']
            + repeat(['#'], &lines)
            + ['enddef']
        lines->setline(1)
        autocmd VimEnter * OnVimEnter()
        def OnVimEnter()
            set filetype=vim
            search('0}')
            normal! zz
        enddef
    EOF
    )

Press `a` to enter insert mode, then `Enter` to insert a linebreak before `}`.
The view is completely changed (topline increases).

<https://github.com/andymass/vim-matchup/issues/132#issuecomment-782770233>

Is it a Vim bug?

Update: It's probably caused by the default Vim indent plugin which uses the `%`
mapped by the matchparen plugin:

    silent! normal %
                  ^
                  ✘
                  no bang

##
## Issues specific to the script level
### ?

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

No error is given,  but `E117` should be given if the function  was local to the
block.

Related issue: <https://github.com/vim/vim/issues/6498>

---

Although, if possible, it should not break sth like this:

    if stridx(&rtp, '/lg-lib,') != -1
        import Derive from 'lg/syntax.vim'
    endif
    Derive(...)

That is, `Derive()` should be still local to the script, not to the `if` block.

Update: I don't think it would be a good idea.
For example, this wouldn't work anymore:

    if has('textprop')

      def RemoveHighlight()
        silent! prop_remove({type: 'matchparen', all: true}, line('w0'), line('w$'))
      enddef

    else

      def RemoveHighlight()
        if get(w:, 'matchparen') != 0
          silent! matchdelete(w:matchparen)
          w:matchparen = 0
        endif
      enddef

    endif

### ?

From `:h E1050 /exit_cb`:

   > Since a continuation line cannot be easily recognized the parsing of commands
   > has been made stricter.  E.g., because of the error in the first line, the
   > second line is seen as a separate command: >
   >         popup_create(some invalid expression, {
   >            exit_cb: Func})
   > Now "exit_cb: Func})" is actually a valid command: save any changes to the
   > file "_cb: Func})" and exit.  To avoid this kind of mistake in Vim9 script
   > there must be white space between most command names and the argument.

I *think* this explanation was relevant when Vim didn't abort after encountering
an error while sourcing a script; it kept sourcing until the end.
However, this issue has been fixed in 8.2.2817.
So, is the example given in this excerpt from the help still relevant?
Maybe it needs to be removed.
We could  still say  that a  whitespace between  a command  and its  argument is
required because it improves readability:

    d_
    ^^
    what's this "_"? is it part of the command name

    d _
      ^
      ok, it's not part of the command name, so it must be an argument

Unless we can  find another example where  the space between a  command name and
its argument prevents an issue...

### ?

    $ vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        def Func( # comment
            a: any,
            b: any
            e: any,
            f: any
            )
            echo 123
        enddef
        Func()
    EOF
    )

    E475: Invalid argument:  # comment

The error message is confusing.
Could Vim tell us that we forgot a comma at the end of the `b: any` line?

---
```vim
vim9script
def Func(a: any, b: any e: any, f: any)
    echo 123
enddef
Func()
```
    E475: Invalid argument: a: any, b: any e: any, f: any)

Again, could Vim be more accurate regarding where the error is coming from?

### ?
```vim
vim9script

eval # some comment
```
    E121: Undefined variable: #

I think a different error should be given.  Maybe `E1143`?
```vim
vim9script

def Func()
    eval # some comment
enddef
defcompile
```
    E1143: Empty expression: "# some comment"

##
## Issues specific to line addresses in error messages
### ?
```vim
vim9script
def Func()
    eval 1 + 0
    eval 2 + 0
    eval 3 + 0
    timer_start(0, (_) => {
        echo 'message'
    )
enddef
```
    Error detected while processing command line..script /proc/42151/fd/17:
    line    2:
    E1171: Missing } after inline function

Maybe the error should be given from the function, rather than from the script.
Unless the error prevents Vim from finding `:enddef`...
But even then, it would help if the line address was closer to the issue (6 or 8).

### ?
```vim
vim9script
[{a: 1, b: ''}]->filter((_, v: dict<number>): bool =>
    true
    # some comment
    )
```
    line    5:
    E1013: Argument 2: type mismatch, expected dict<number> but got dict<any>

I don't  think the line number  is technically wrong  (5), but it would  be more
useful if it matched  the start of the `filter()` call  (2), where the arguments
types are declared, rather than its end.

---

Same issue in a function call:
```vim
vim9script
def Func(n: number)
enddef
Func(

    ''

    )
```
    line    8:
    E1013: Argument 1: type mismatch, expected number but got string

Actually, could Vim be  smarter and give the actual line  number where the wrong
argument is received (i.e. here 6)?

---

Similar issue when the error is in the body of the lambda:
```vim
vim9script
def Func()
    var Rep: func = (m): string =>
                         m[0]->str2nr() > 99
                         ? ''
                         : m[0]->str2nr()
    'pat'->substitute('pat', Rep, '')
enddef
Func()
```
                         v--------v
    Error detected while processing command line..script /proc/17291/fd/11[9]..function <SNR>1_Func[5]..<lambda>1:
    line    1:
    E1012: Type mismatch; expected string but got number

It would be more useful if the reported line number was 3, rather than 1.
Not sure  that can  be done  though; it  seems Vim  joins all  the lines  in the
lambda's definition:

    :function <lambda>1
        def <lambda>1(m: any, ...): string˜
     1  return m[0]->str2nr() > 99                         ? ''                         : m[0]->str2nr()˜
        enddef˜

   > This is quite complicated.  It is also less efficient.  I'm not going to
   > do this now.

Source: <https://github.com/vim/vim/issues/10364#issuecomment-1119701864>

If it can't  be improved when the error  is given at runtime, could  it still be
improved when the error is given at compile time?
```vim
vim9script
def Func()
    var Rep: func = (m): string =>
                         false
                         ? ''
                         : m[0]->str2nr()
    'pat'->substitute('pat', Rep, '')
enddef
defcompile
```
                         v-------v
    Error detected while compiling command line..script /proc/17876/fd/11[9]..function <SNR>1_Func[4]..<lambda>1:
    line    1:
    E1012: Type mismatch; expected string but got number

### ?
```vim
vim9script
echo [[]]->map((_, v) =>
    []
    +
    [][0]
    +
    []
)
```
    Error detected while processing command line..script /tmp/.tmux.run.vim[8]..function <lambda>1:
    line    1:
    E684: List index out of range: 0

The error is given on line 8, which is the *last* line of the lambda:

    Error detected while processing command line..script /tmp/.tmux.run.vim[8]..function <lambda>1:
                                                                            ^

Wouldn't it be better to give the error on the *first* line?

    Error detected while processing command line..script /tmp/.tmux.run.vim[2]..function <lambda>1:
                                                                            ^

##
## to document: closures work with `function()`, but not with lambdas
### `function()`
#### argument scope
```vim
vim9script
def Setup(name: string)
    &operatorfunc = function(Opfunc, [name])
enddef

def Opfunc(name: string, _)
    echomsg name
enddef

Setup('no error')
normal! g@l
```
    no error

#### function scope
```vim
vim9script
def Setup()
    var name: string = 'no error'
    &operatorfunc = function(Opfunc, [name])
enddef

def Opfunc(name: string, _)
    echomsg name
enddef

Setup()
normal! g@l
```
    no error

###
### lambda
#### argument scope
```vim
vim9script
def Setup(name: string)
    &operatorfunc = (_) => Opfunc(name)
enddef

def Opfunc(name: string)
    echomsg name
enddef

Setup('error')
normal! g@l
```
    E1248: Closure called from invalid context

#### function scope
```vim
vim9script
def Setup()
    var name: string = 'error'
    &operatorfunc = (_) => Opfunc(name)
enddef

def Opfunc(name: string)
    echomsg name
enddef

Setup()
normal! g@l
```
    E1248: Closure called from invalid context

##
## Vim9: cannot use Vim9 syntax to undo settings from filetype/indent plugins

**Is your feature request about something that is currently impossible or hard to do? Please describe the problem.**

We cannot use the Vim9 syntax when we need to undo settings from filetype/indent plugins.

That's because the contents of `b:undo_ftplugin` is run in the legacy context:

    legacy exe b:undo_ftplugin
    ^----^

[source](https://github.com/vim/vim/blob/31e5c60a682840959cae6273ccadd9aae48c928d/runtime/ftplugin.vim#L25)

Same thing with `b:undo_indent`:

    legacy exe b:undo_indent
    ^----^

[source](https://github.com/vim/vim/blob/31e5c60a682840959cae6273ccadd9aae48c928d/runtime/indent.vim#L17)

Besides, setting those variables correctly is too tricky.  See [this issue](https://github.com/vim/vim/issues/9645) for more info.  The root cause comes from the data type of the `b:undo_*` variables: a list would be better than a string.

**Describe the solution you'd like**

Introduce 2 new variables: `b:undo_ftplugin_list` and `b:undo_indent_list`.
Those variables would be meant to be assigned a list of funcrefs/lambdas/strings.

A list is better suited than a string because the code which undoes local settings is not necessarily read from a single script.  It can be read from several.  For example, we can have these 2 scripts:

   - `$VIMRUNTIME/ftplugin/c.vim`
   - `$HOME/.vim/after/ftplugin/c.vim`.

Each of them can set options, and undo settings for the C filetype.  And it's easier to append to a list than to a string (again, see #9645).

The benefit of a funcref/lambda is that it's processed in the context of the script where it is defined.  We can leverage this feature to allow the Vim9 syntax when undoing settings.

**Describe alternatives you've considered**

N/A

**Additional context**

As a suggestion, here is a patch:
```diff
diff --git a/runtime/doc/usr_41.txt b/runtime/doc/usr_41.txt
index eb269e16c..21fe47a83 100644
--- a/runtime/doc/usr_41.txt
+++ b/runtime/doc/usr_41.txt
@@ -2514,6 +2514,17 @@ be set accordingly.

 Both these variables use legacy script syntax, not |Vim9| syntax.

+				*undo_indent_list* *undo_ftplugin_list*
+
+Alternatively, you can set the b:undo_ftplugin_list variable with a list of
+strings and funcrefs or lambdas.  Example: >
+
+	# in a Vim9 script
+	b:undo_ftplugin_list += ['setlocal commentstring<', () => MyUndoFunc()]
+
+Note that the string items are executed with the legacy syntax.  But the
+funcrefs/lambdas are executed in the context of the script where they are
+defined; this is useful if one of your commands needs to use the Vim9 syntax.

 FILE NAME

diff --git a/runtime/ftplugin.vim b/runtime/ftplugin.vim
index 2500a7f27..908fae5df 100644
--- a/runtime/ftplugin.vim
+++ b/runtime/ftplugin.vim
@@ -26,6 +26,23 @@ def LoadFTPlugin()
     unlet! b:undo_ftplugin b:did_ftplugin
   endif

+  if !exists('b:undo_ftplugin_list')
+    if &filetype != ''
+      b:undo_ftplugin_list = []
+    endif
+  else
+    if type(b:undo_ftplugin_list) == v:t_list
+      for Item in b:undo_ftplugin_list
+        if type(Item) == v:t_string
+          legacy execute Item
+        elseif type(Item) == v:t_func
+          call(Item, [])
+        endif
+      endfor
+    endif
+    unlet! b:undo_ftplugin_list
+  endif
+
   var s = expand("<amatch>")
   if s != ""
     if &cpo =~# "S" && exists("b:did_ftplugin")
diff --git a/runtime/indent.vim b/runtime/indent.vim
index a3249956a..3709f7870 100644
--- a/runtime/indent.vim
+++ b/runtime/indent.vim
@@ -17,6 +17,24 @@ def s:LoadIndent()
     legacy exe b:undo_indent
     unlet! b:undo_indent b:did_indent
   endif
+
+  if !exists('b:undo_indent_list')
+    if &filetype != ''
+      b:undo_indent_list = []
+    endif
+  else
+    if type(b:undo_indent_list) == v:t_list
+      for Item in b:undo_indent_list
+        if type(Item) == v:t_string
+          legacy execute Item
+        elseif type(Item) == v:t_func
+          call(Item, [])
+        endif
+      endfor
+    endif
+    unlet! b:undo_indent_list
+  endif
+
   var s = expand("<amatch>")
   if s != ""
     if exists("b:did_indent")
```
---

As extra benefits, these variables would let us write a code which is:

   - more reliable (see issue #9645)
   - easier to write (because nesting a mix of quotes inside a string is tricky)
   - easier to read (because with a funcref/lambda we don't lose syntax highlighting, contrary to a string)

As an example, compare this (copied from `$VIMRUNTIME/ftplugin/c.vim`):
```vim
let b:undo_ftplugin = "setl fo< com< ofu< cms< def< inc< | if has('vms') | setl isk< | endif"
```
To this:
```vim
vim9script
b:undo_ftplugin_list = [() => {
   setlocal formatoptions<
   setlocal comments<
   setlocal omnifunc<
   setlocal commentstring<
   setlocal define<
   setlocal include<
   if has('vms')
     setlocal iskeyword<
   endif
}]
```
It's subjective, but I prefer reading the 2nd one.

The current closest alternative is this:
```vim
let b:undo_ftplugin_list = 'call MyUndoFunc()'
def g:MyUndoFunc()
   setlocal formatoptions<
   setlocal comments<
   setlocal omnifunc<
   setlocal commentstring<
   setlocal define<
   setlocal include<
   if has('vms')
     setlocal iskeyword<
   endif
enddef
```
But:

   - this requires polluting the global namespace with a new function (where the risk of a conflict is always present)
   - this still forces us to use some legacy syntax (namely the `:call` command)

## ?

<https://github.com/vim/vim/issues/9802#issuecomment-1047828858>

The issue is fixed for `map()`, `filter()`, and `sort()`.
But it probably persists for `setqflist()`, `matchfuzzy()`, and `matchfuzzypos()`.
And what about those:

  - `:help call()`
  - `:help eval()`
  - `:help function()`
  - `:help search()`
  - `:help searchpair()`
  - `:help searchpairpos()`
  - `:help substitute()`
  - `:help timer_start()`

## ?

Try to replace as many `mapnew()` with `map()`.

## Look for commands which should be passed an argument but don't give any error when they aren't

## We can't use the dot notation to call an imported autoloaded function in some contexts.

   - `:help i_CTRL-R_=` (11)
   - `:help c_CTRL-\_e` (9)
   - `:help stl-%{` (6)
   - `:help 'statusline'` (1) and `:help 'tabline'` (`%!Func()`)
   - `:help input()` (3rd `{completion}` argument)

Should it be made to work?
Should we document these limitations somewhere in the help?

The issue is that those syntaxes are evaluated in the global context.

Are there  other syntaxes where the  global context is used,  causing unexpected
issues if they contain Vim9 expressions?
What about setting a `*func` option?  Can we use `script.func` over there?
Note that it works for `*expr` options.

I think that –  if it's possible – Vim should save  somewhere the context in
which the expression was set.  It would make sense, avoid unexpected errors, and
be consistent with what will happen in the future for options:

   > Use the location where the option was set for deciding whether it's to be
   > evaluated in Vim9 script context.

Source: `:help todo`.

---

To  refactor  the   remaining  autoload  function  names   from  `foo#Bar()`  to
`foo.Bar()`, source this script:

    vim9script
    var pat: string = '\Cexport def'
    execute printf('Cvim ;%s;gj $MYVIMRC ~/.vim/**/*.vim ~/.vim/**/*.snippets ~/.vim/template/**', pat)
    autocmd QuickFixCmdPost * ++once OnQuickFixCmdPost()
    def OnQuickFixCmdPost()
        execute 'silent Cfilter! -vendor'
        execute 'silent Cfilter! -tmp'
        execute 'silent Cfilter! netrwPlugin\.vim'
        execute 'silent Cfilter! netrw\.vim'
        execute 'silent Cfilter! tmuxify\.vim'
        execute 'silent Cfilter! netrwFileHandlers\.vim'
        execute 'silent Cfilter! netrwSettings\.vim'
        execute 'silent Cfilter! netrw_gitignore\.vim'
    enddef

---

    :s/def \<[a-zA-Z_]\+#[a-zA-Z_0-9#]\+\ze(/\='export def ' .. submatch(0)->matchstr('#[^#]\+$')->substitute('#\(.\)', {-> submatch(1)->toupper()}, '')/

    :s/\<[a-zA-Z_]\+#[a-zA-Z_0-9#]\+\ze[(', \n]/\=submatch(0)->matchstr('[^#]\+#[^#]\+$')->substitute('#\(.\)', {-> '.' .. submatch(1)->toupper()}, '')/

## ctags

`ctags(1)` does not generate any tag for variables declared with `:var`.

Send a patch which refactors this line:

    // $HOME/VCS/ctags/parsers/vim.c
    else if (wordMatchLen (line, "let", 3))

Into this line:

    else if (wordMatchLen (line, "let", 3) || wordMatchLen (line, "var", 3))

But only for variables declared at the script level.
To be  consistent with how  legacy scripts are parsed  (function-local variables
are ignored).

---

Do the same for `:final`.

---

Do the same for *exported* `:def` functions.

---

Also, the tags which are currently generated for `:const` are not always correct.
For example, the tag generated for this line:

    const MYCONST: number = 123

looks like this:

    MYCONST:	path/to/file	/^const MYCONST: number = 123$/;"	C
           ^
           ✘

The colon should not be there.  Because of this, when we press on a reference to
a constant name with `C-]`, Vim fails to jump to its declaration.

The same issue will affect the tags generated for variables declared with `:var`
(and `:final`).  I think you need to refactor this function:

    // $HOME/VCS/ctags/parsers/vim.c
    parseVariableOrConstant()

In particular, this line:

    } while (isalnum ((int) *cp) || *cp == '_' || *cp == '#' || *cp == ':' || *cp == '$');
                                                                ^--------^

Find a way to make this condition stricter.
We should not accept a colon if there is nothing after (or a space).
I think the next character can be referred to with `*np`.
But none of these work:

    *cp == ':'
    →
    (*cp == ':' && *np == ' ')

    *cp == ':'
    →
    (*cp == ':' && *np == '$')

To debug:

    $ cd ~/VCS/ctags/
    $ make clean; make distclean; ./autogen.sh; ./configure; sed -i 's/^CFLAGS =.*/CFLAGS = -g -O0/; s/^CFLAGS_FOR_BUILD =.*/CFLAGS_FOR_BUILD = -g -O0/' Makefile; make
    $ cd /tmp/vim_plugin/
    $ gdb -q --args ~/VCS/ctags/ctags --options=NONE -R .
    (gdb) break parsers/vim.c:parseVariableOrConstant
    (gdb) run

Update: This patch seems to work:
```diff
diff --git a/parsers/vim.c b/parsers/vim.c
index da4188d4..66d673f2 100644
--- a/parsers/vim.c
+++ b/parsers/vim.c
@@ -546,7 +546,7 @@ static void parseVariableOrConstant (const unsigned char *line, int infunction,

 			vStringPut (name, (int) *cp);
 			++cp;
-		} while (isalnum ((int) *cp) || *cp == '_' || *cp == '#' || *cp == ':' || *cp == '$');
+		} while (isalnum ((int) *cp) || *cp == '_' || *cp == '#' || (*cp == ':' && *cp++ != ':') || *cp == '$');
 		makeSimpleTag (name, kindIndex);
 		vStringClear (name);
 	}
```
But is it really correct?
Update: I think it's wrong because `*cp++` has a side effect.
Maybe we need to make a copy of `cp` in the loop:

    np = cp;
    ++np;

---

Try to be consistent when using the `s:` prefix.
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
---

Watch the derek banas playlist on C  to have just enough knowledge to understand
the code and refactor it.

To test:

    $ rm -rf /tmp/vim_plugin/
    $ mkdir -p /tmp/vim_plugin
    $ cd /tmp/vim_plugin

    $ tee <<'EOF' >foo.vim
        vim9script
        const NAME_A: number = 123
        export const NAME_B: number = 456
        def FuncA()
        enddef
        export def FuncB()
        enddef
    EOF

    $ cd ~/VCS/ctags/
    $ ./autogen.sh
    $ ./configure
    $ make
    $ cd /tmp/vim_plugin/
    $ ~/VCS/ctags/ctags --options=NONE -R .
    $ vim tags

---

In this function:

    static bool isMap (const unsigned char *line)

`tnoremap` and `tmap` are missing.

## Test all builtin functions which accept a string with a special meaning as argument.

   > .	    the cursor position
   > $	    the last line in the current buffer
   > 'x	    position of mark x (if the mark is not set, 0 is
   >         returned)
   > w0	    first line visible in current window (one if the
   >         display isn't updated, e.g. in silent Ex mode)
   > w$	    last line visible in current window (this is one
   >         less than "w0" if no lines are visible)
   > v	    In Visual mode: the start of the Visual area (the
   >         cursor is the end).  When not in Visual mode
   >         returns the cursor position.  Differs from |'<| in
   >         that it's updated right away.

---

    append()
    appendbufline({expr}, {lnum}, {text})
    cursor()
    deletebufline({buf}, {first} [, {last}])
    diff_filler()
    diff_hlID({lnum}, {col})
    foldclosed()
    foldclosedend()
    foldlevel()
    foldtextresult()
    getbufline({buf}, {lnum} [, {end}])
    getline({lnum})                     String  line {lnum} of current buffer
    getline({lnum}, {end})              List    lines {lnum} to {end} of current buffer
    getpos()
    indent()
    line({expr} [, {winid}])    Number  line nr of cursor, last line or mark
    line2byte()
    lispindent()
    nextnonblank()
    setbufline({expr}, {lnum}, {text})
    setline({lnum}, {line})             Number  set line {lnum} to {line}
    synID()
    synconcealed()
    synstack()
    term_getline({buf}, {row})  String  get a line of text from a terminal

---

    ~/line.vim

---

Test `col()` and friends.

##
## autoload
### unquoted autoloaded functions are sourced as soon as encountered

This needs to be documented:
<https://github.com/vim/vim/issues/8124#issuecomment-823951731>

Also, if you set a `*func` option to  a funcref for an autoload function (at the
script  level,  or in  a  `:def`  function  if  `:defcompile` is  run),  without
surrounding the funcname with quotes, its autoload script is sourced immediately
(which is bad for startup time).  Again, this should be documented.

BTW, does this remain true if we use a lambda instead?
What about a partial?

---

This excerpt from the help looks wrong:

   > When compiling a `:def` function and a function in an autoload script is
   > encountered, the script is not loaded until the `:def` function is called.

That's true only if the name of the autoload function is quoted.
Also, "a function in an autoload script" might be misunderstood:

   - a function which is defined in an autoload script?
   - a function which is encountered while reading an autoload script?

"an autoloaded function" is better.

### ?

<https://github.com/vim/vim/issues/9590#issuecomment-1019080740>

The issue was fixed, but the inconsistency reported in this comment still persists.
Open an issue to discuss how we could improve the help about autoload functions.
i.e. We need to make it clearer how quotes are important.
In this issue, discuss whether the previously mentioned inconsistency is intended.
```vim
vim9script
var dir = '/tmp/.vim'
dir->delete('rf')
&runtimepath = dir
dir ..= '/autoload'
dir->mkdir('p')
var lines =<< trim END
    vim9script
    export def Func()
        echomsg 'from Func()'
    enddef
    sleep 5
END
lines->writefile(dir .. '/script.vim')
import autoload 'script.vim'
def Foo()
    call(script#Func, [])
enddef
defcompile
```
    the code compiles after 5 seconds
```vim
vim9script
var dir = '/tmp/.vim'
dir->delete('rf')
&runtimepath = dir
dir ..= '/autoload'
dir->mkdir('p')
var lines =<< trim END
    vim9script
    export def Func()
        echomsg 'from Func()'
    enddef
    sleep 5
END
lines->writefile(dir .. '/script.vim')
import autoload 'script.vim'
def Foo()
    call(script.Func, [])
enddef
defcompile
```
    the code compiles immediately

Update: Working as intended:
<https://github.com/vim/vim/issues/9966#issuecomment-1072464669>

Conclusion: Avoid `script#Func`.  Prefer `script.Func`.
And at the script  level, make sure to quote `script.Func`;  in compiled code do
whatever you want (quote or not).

##
## ?

<https://github.com/vim/vim/issues/8092#issuecomment-1001077485>

Check whether the issue #8092 is fixed for:

   - `matchfuzzy()` (key `text_cb`)
   - `searchpair()`
   - `setqflist()` (key `quickfixtextfunc`)
   - `sort()`
   - `substitute()`
   - `timer_start()`

## ?

To document.
```vim
vim9script
def Func()
    var d: list<dict<any>> = [{a: 0}]
    for e in d
        e = {}
    endfor
enddef
Func()
```
    E1018: Cannot assign to a constant: e
```vim
vim9script
def Func()
    var l: list<dict<any>> = [{a: 0}]
    for e in l
        e.b = ''
    endfor
    echo l
enddef
Func()
```
    [{'a': 0, 'b': ''}]

This might explain the rationale behind the different results:
<https://stackoverflow.com/a/7838212>

## ?

   > incomplete or wrong error message when executing ambiguous Ex command

<https://github.com/vim/vim/issues/9564#issuecomment-1017726136>

## ?

We can set an opfunc in Vim9 or in legacy (2).
We can set an opfunc with `:set` or with `&`/`:let` (2).
We can set an opfunc at the script level or in a function (2).
We can set an opfunc with a name, a funcref, a lambda (closure or not), or a partial (closure or not) (6).

2 x 2 x 2 x 6 = 48 tests.

Also, the  funcref/partial can  be to  a function local  to the  script, global,
autoloaded.

48 x 3 = 144 tests.

---

If `CountSpaces()` is local to the script, this doesn't work in a Vim9 script:

    set operatorfunc=CountSpaces

Neither at the script level, nor in a function.
That's because `CountSpaces` is only looked for in the global namespace.
Solution:

    &operatorfunc = CountSpaces

---

A lambda closure doesn't work in Vim9:

    def ...
        var n = 123
        &operatorfunc = (t) => CountSpaces(n, t)
                                           ^
                                           ✘
        ...

---
```vim
vim9script
def CountSpaces(type = ''): string
    if type == ''
        return 'g@'
    endif
    normal! '[V']y
    echomsg getreg('"')->count(' ')
    return ''
enddef
set operatorfunc=CountSpaces
nnoremap <expr> <F4> CountSpaces()
['a b c d e']->setline(1)
feedkeys("\<F4>_")
```
    E117: Unknown function: CountSpaces
```vim
vim9script
def CountSpaces(type = ''): string
    if type == ''
        return 'g@'
    endif
    normal! '[V']y
    echomsg getreg('"')->count(' ')
    return ''
enddef
&operatorfunc = CountSpaces
nnoremap <expr> <F4> CountSpaces()
['a b c d e']->setline(1)
feedkeys("\<F4>_")
```
    4
```vim
vim9script
def CountSpaces(type = ''): string
    if type == ''
        return 'g@'
    endif
    normal! '[V']y
    echomsg getreg('"')->count(' ')
    return ''
enddef
&operatorfunc = (t) => CountSpaces(t)
nnoremap <expr> <F4> CountSpaces()
['a b c d e']->setline(1)
feedkeys("\<F4>_")
```
    4
```vim
vim9script
def CountSpaces(free = 0, type = ''): string
    if type == ''
        return 'g@'
    endif
    normal! '[V']y
    echomsg f
    echomsg getreg('"')->count(' ')
    return ''
enddef
var f = 123
&operatorfunc = (t) => CountSpaces(f, t)
nnoremap <expr> <F4> CountSpaces()
['a b c d e']->setline(1)
feedkeys("\<F4>_")
```
    123
    4
```vim
vim9script
def CountSpaces(type = ''): string
    if type == ''
        return 'g@'
    endif
    normal! '[V']y
    echomsg getreg('"')->count(' ')
    return ''
enddef
&operatorfunc = function(CountSpaces)
nnoremap <expr> <F4> CountSpaces()
['a b c d e']->setline(1)
feedkeys("\<F4>_")
```
    4
```vim
vim9script
def CountSpaces(free = 0, type = ''): string
    if type == ''
        return 'g@'
    endif
    echomsg f
    normal! '[V']y
    echomsg getreg('"')->count(' ')
    return ''
enddef
var f = 123
&operatorfunc = function(CountSpaces, [f])
nnoremap <expr> <F4> CountSpaces()
['a b c d e']->setline(1)
feedkeys("\<F4>_")
```
    123
    4

## ?

Could `'*expr'` options accept lambdas and partials in the future?
```vim
vim9script
&foldexpr = () => getline(v:lnum) =~ '^#' ? '>1' : '1'
&foldmethod = 'expr'
&debug = 'throw'
```
    E729: Using a Funcref as a String
    E928: String required

Relevant PR: <https://github.com/vim/vim/pull/9401>

---

BTW, what about `input()`?
```vim
vim9script
var lines: list<string> =<< trim END
    the quick brown fox
    jumps over the lazy dog
END
lines->setline(1)
def CompleteWords(_a: any, _l: any, _p: any): string
    return getline(1, '$')
        ->join(' ')
        ->split('\s\+')
        ->filter((_, v) => v =~ '^\a\k\+$')
        ->sort()
        ->uniq()
        ->join("\n")
enddef
var word: string = input('word: ', '', 'custom,' .. expand('<SID>') .. 'CompleteWords')
```
We need  `expand('<SID>')`.  In Vim9,  could Vim  look in the  global namespace,
*then*  in  the  script-local  one   when  we  specify  `CompleteWords`  without
`expand('<SID>')`.

## ?

Read (and test?) test tests:

   - [8.2.3619](https://github.com/vim/vim/releases/tag/v8.2.3619)  cannot use a lambda for 'operatorfunc'
   - [8.2.3665](https://github.com/vim/vim/releases/tag/v8.2.3665)  cannot use a lambda for 'tagfunc'
   - [8.2.3712](https://github.com/vim/vim/releases/tag/v8.2.3712)  cannot use Vim9 lambda for 'tagfunc'
   - [8.2.3725](https://github.com/vim/vim/releases/tag/v8.2.3725)  cannot use a lambda for 'completefunc' and 'omnifunc'
   - [8.2.3735](https://github.com/vim/vim/releases/tag/v8.2.3735)  cannot use a lambda for 'imactivatefunc'
   - [8.2.3751](https://github.com/vim/vim/releases/tag/v8.2.3751)  cannot assign a lambda to an option that takes a function
   - [8.2.3756](https://github.com/vim/vim/releases/tag/v8.2.3756)  might crash when callback is not valid
   - [8.2.3758](https://github.com/vim/vim/releases/tag/v8.2.3758)  options that take a function insufficiently tested
   - [8.2.3788](https://github.com/vim/vim/releases/tag/v8.2.3788)  lambda for option that is a function may be freed
   - [8.2.3792](https://github.com/vim/vim/releases/tag/v8.2.3792)  setting *func options insufficiently tested

## :help modifyOtherKeys

The tip to disable the feature, using a `:!` command is a bit hacky.
Using `echoraw()` is seems more reliable and easier to understand.

---

Doesn't work well with tmux.

---

The handling of `<C-A>` vs `<M-A>` is inconsistent when modifyOtherKeys is enabled.

In `~/.vim/pack/mine/opt/lg-lib/import/lg/map.vim`:

    # For some reason, in GUI and when modifyOtherKeys is enabled, Vim conflates `<M-X>` with `<M-S-X>`.
    #
    # In conjunction with `<unique>`, this can lead to unexpected errors:
    #
    #     $ vim -Nu NONE -g +'nnoremap <unique> <M-G> <cmd>echo "M-G"<CR>' \
    #                       +'nnoremap <unique> <M-S-G> <cmd>echo "M-S-G"<cr>'
    #     E227: mapping already exists for Ç˜
    #
    # To avoid this, let's make sure that in `<M-x>`, the `x` is lowercase.

Is this a known bug?

I think this pitfall was mentioned here <https://github.com/vim/vim/issues/6457>.
It might not be a bug, but at least it should be documented.

Update: I think it's a bug, because it's handled inconsistently between the CTRL
and the META modifiers:

    $ vim -Nu NONE +'nnoremap <C-A> <Cmd>echo "C-A"<CR>'
    # press CTRL-A
    # Expected: "C-A" is printed on the command-line
    # Actual: "C-A" is printed on the command-line
    ✔

    $ vim -Nu NONE +'nnoremap <M-A> <Cmd>echo "M-A"<CR>'
    # press ALT-A
    # Expected: "M-A" is printed on the command-line
    # Actual: nothing is printed on the command-line
    ✘

IOW, in  the GUI  and when modifyOtherKeys  is enabled, in  a mapping  whose lhs
contains a modifier combined with a letter,  the case of the latter matters with
META (then, it  implies `S-`), but it  does not matter with CTRL  (`S-` is never
implied).

## :help :script
```diff
diff --git a/runtime/doc/repeat.txt b/runtime/doc/repeat.txt
index 049fabb30..0889b7d98 100644
--- a/runtime/doc/repeat.txt
+++ b/runtime/doc/repeat.txt
@@ -383,8 +383,8 @@ For writing a Vim script, see chapter 41 of the user manual |usr_41.txt|.
 			feature}

 :scr[iptnames][!] {scriptId}			*:script*
-			Edit script {scriptId}.  Although ":scriptnames name"
-			works, using ":script name" is recommended.
+			Edit script {scriptId}.  Although ":scriptnames ID"
+			works, using ":script ID" is recommended.
 			When the current buffer can't be |abandon|ed and the !
 			is not present, the command fails.

```
## <F1..4> don't work with modifiers in xterm

Same issue with `<Del>`.

<https://github.com/vim/vim/issues/9131#issuecomment-967774895>

## â modifyOtherKeys

<https://github.com/vim/vim/issues/5951>

The issue is badly presented.  Close it and open a new one.
Indeed, the title is wrong.  Here is a better one:

   > cannot use dead key to insert accented character before using modifier

Provide a  log obtained with `ch_logfile()`,  showing that the issue  is in Vim;
not in the OS/system input/terminal/...  That is, whether you insert `â` before
or after having pressed a modifier combined  with another key, in both cases Vim
receives the same raw input sequence: `â`.

Also, we might have found some hacky workaround:

    ✔
    vim -Nu NONE --cmd 'inoremap <Esc>[27;5;59~ <Nop>' +'inoremap <M-b> xxx' +'startinsert' +'call feedkeys("\<Esc>[27;5;59~")'

    ✘
    vim -Nu NONE -S <(tee <<'EOF'
        inoremap <Esc>[27;5;59~ <Nop>
        inoremap <M-b> xxx
        autocmd InsertEnter * ++once call feedkeys("\<Esc>[27;5;59~")
    EOF
    )

    ✔
    vim -Nu NONE -S <(tee <<'EOF'
        inoremap <Esc>[27;5;59~ <Nop>
        inoremap <M-b> xxx
        startinsert
        call feedkeys("\<Esc>[27;5;59~")
    EOF
    )

    ✔
    vim -Nu NONE -S <(tee <<'EOF'
        inoremap <M-b> xxx
        call feedkeys("\<Esc>[27;5;0~")
    EOF
    )

    ✘
    vim -Nu NONE -S <(tee <<'EOF'
        inoremap <M-b> xxx
        call echoraw("\<Esc>[27;5;0~")
    EOF
    )

## vim-stacktrace

   > is there a way to get vim to report absolute line file numbers rather than lines in a function for errors
   > within a function? I'm getting tired trying to work it out.

Could it be done for the next Vim9 release?
Alternatively, we should probably at least provide a default optional package to
populate the quickfix list with Vimscript errors (`:packadd ...`).

Find another similar quote from a reddit thread where people criticize Vimscript.

## ?
```vim
vim9script
var name: number
def Func()
  if rand() % 2
      name = ''
  else
  endif
enddef
defcompile
```
    E1012: Type mismatch; expected number but got string
    ✔
```vim
vim9script
var name: number
def Func()
  if rand() % 2
  else
      name = ''
  endif
enddef
defcompile
```
    E1012: Type mismatch; expected number but got string
    ✔
```vim
vim9script
var name: number
def Func()
  if has('sound')
      name = ''
  else
  endif
enddef
defcompile
```
    E1012: Type mismatch; expected number but got string
    ✔
```vim
vim9script
var name: number
def Func()
  if has('sound')
  else
      name = ''
  endif
enddef
defcompile
```
    no error
    ✘

Is that really a bug?
See `:help vim9 /vim9-gotchas/;/has(`.

Update: It seems the last snippet is equivalent to:
```vim
vim9script
var name: number
def Func()
  if false
      name = ''
  endif
enddef
defcompile
```
    no error
    ✘

So, IIUC,  at compile time, if  Vim finds some  code which it knows  for certain
that it won't run at runtime, then it doesn't compile it:
```vim
vim9script
if false
    invalid
endif
echo 'no error'
```
    no error
```vim
vim9script
def Func()
    if false
        invalid
    endif
enddef
Func()
echo 'no error'
```
    no error

Doesn't this contradict:

   > Vim9 functions are compiled as a whole: >

Is it documented?  Should it?

I guess it can be inferred from this:

   > Or put the unsupported code inside an `if` with a constant expression that
   > evaluates to false: >
   >         def Maybe()
   >           if has('feature')
   >             use-feature
   >           endif
   >         enddef

---

Review the remaining TODOs/FIXMEs in killersheep.
Finish refactoring?

## ?

Make more tests to be sure that it would be OK to automatically set `<FocusGained>` and `<FocusLost>` in all popular terminals as well as `ttymouse=xterm`:

   <https://github.com/vim/vim/issues/9296#issuecomment-989144666>
   > A side effect is that 'ttymouse' will default to "xterm". Is that OK?

Post your findings on this thread:
<https://github.com/vim/vim/issues/9296#issuecomment-989156732>

Close it once a decision has been made and the help has been updated:

   <https://github.com/vim/vim/issues/9296#issuecomment-989144666>
   > We should update the help to mention setting <FocusGained> and <FocusLost>.

## ?

   <https://github.com/vim/vim/issues/9309#issuecomment-989802176>
   > At some point, we might want to document how to generate log files for the regex engine:

## ?

Vim9 now supports list declaration in :def functions.
Look for this pattern everywhere:

    \[.*\s=\s\[

Use the syntax whenever it's appropriate.

## ?

Usually, when we write this:

    &option

And the option is local, we want to only set the local value.  Not the global one.
But Vim sets both.
```vim
&colorcolumn = '123'
echo [&l:colorcolumn, &g:colorcolumn]
```
    ['123', '123']

Could Vim set only the local value?
Otherwise, we always have to write `l:`:

    &l:colorcolumn = '123'
     ^^

Which looks weird/awkward.

## Vim9: sourcing Vim9 script before vimrc keeps 'cpoptions' to Vi default value

**Steps to reproduce**

Run this shell command:

    $ echo 'vim9script' >/tmp/t.vim && \
        VIMINIT='source /dev/null' vim --cmd 'source /tmp/t.vim' +'echomsg &cpoptions'

This is echo'ed:

    aAbBcCdDeEfFgHiIjJkKlLmMnoOpPqrRsStuvwWxXyZ$!%*-+<>;

That is the Vi default value of `'cpoptions'`.

**Expected behavior**

This is echo'ed:

    aABceFs

That is the Vim (!= Vi) default value of `'cpoptions'`, because:

   1. a vimrc is found (`/dev/null`)
   2. therefore, `'compatible'` is reset
   3. therefore, `'cpoptions'` is set to the Vim default value

**Operating system**

Ubuntu 20.04.3 LTS

**Version of Vim**

8.2 Included patches: 1-3731

**Additional Context**

The usage of `VIMINIT` might seem contrived but there is a reason for this.
While I'm trying to find a MRE for an issue, I'm often running something like this shell command:

    vim --cmd 'filetype on'

The result is a huge amount of errors (mainly `E10`) which are caused by `'cpoptions'` whose value has been reset to the Vi default value.  These errors are *very* confusing (especially while debugging another issue).

---

The issue cannot be reproduced with `-u`, nor with `-Nu`, because those flags explicitly set or reset `'compatible'`, which in turn set `'cpoptions'`.

---

The issue disappears if the script which is sourced before the vimrc is a legacy script:

    echo '" this is a legacy script' >/tmp/t.vim && \
        VIMINIT='source /dev/null' vim --cmd 'source /tmp/t.vim' +'echomsg &cpoptions'

    aABceFs

---

Why does sourcing any Vim9 script *before* the vimrc prevents `'cpoptions'` from being set to its Vim default value?
And why doesn't it happen also when sourcing a legacy script?  This seems inconsistent.

---

Update:

    # temporarily empty the vimrc
    $ vim --cmd 'set rtp-=~/.vim' +'echo &cpoptions'
    aABceFs
    ✔

    $ vim --cmd 'set rtp-=~/.vim | filetype on' +'echo &cpoptions'
    aAbBcCdDeEfFgHiIjJkKlLmMnoOpPqrRsStuvwWxXyZ$!%*-+<>;
    ✘

There is no Vim9 script involved in the last command.
What's going on here?

Update: `:filetype on` causes `$VIMRUNTIME/filetype.vim` to be sourced.
The latter contains this line:

    let &cpo = s:cpo_save

I think that's the problematic  line, because `s:cpo_save` contains the original
value of `&cpo` which – at the time – still has all the flags.
IOW, the last shell command is equivalent to:

    $ vim --cmd 'set rtp-=~/.vim | let &cpo = "aAbBcCdDeEfFgHiIjJkKlLmMnoOpPqrRsStuvwWxXyZ$!%*-+<>;"' +'echo &cpoptions'
    aAbBcCdDeEfFgHiIjJkKlLmMnoOpPqrRsStuvwWxXyZ$!%*-+<>;
    ✘

---

Read: <https://github.com/vim/vim/issues/9403#issuecomment-1001019804>

And: [8.2.3901](https://github.com/vim/vim/releases/tag/v8.2.3901)
    Problem:    Vim9: Cannot set 'cpo' in main .vimrc if using Vim9 script.
    Solution:   Do not restore 'cpo' at the end of the main .vimrc.

## ?

Write this in a Vim file:

    vim9script
    echo len(0)

Then, execute:

    set filetype=forth
    syntax clear
    set filetype=vim

Notice how the `len` keyword is wrongly highlighted as an error.
That's because `'iskeyword'` has been wrongly altered by the forth syntax plugin.
There are many other syntax plugins making the same mistake.
Instead, they should write:

    if (v:version == 704 && has('patch-7.4.1142')) || v:version > 704
        syntax iskeyword new_value
    else
        setlocal iskeyword=new_value
    endif

But there might be a deeper cause in `$VIMRUNTIME/ftplugin/vim.vim`:

    setlocal isk+=#
                ^^

Why appending to the current value without resetting first?

    # first, we reset
    setlocal isk&vim
    # now, we can append
    setlocal isk+=#

There  are  many  other  filetype  plugins  which  add/remove  an  item  from  a
comma-separated list  of values  in an option.   Should Vim  automatically reset
all/some local options when changing the filetype of a file?
At  least  the most  commonly  set  ones, and  the  most  problematic ones  like
`'iskeyword'`?

Update: I think that's to support dot separated filetypes, like this one:

    set filetype=c.doxygen

## ?

   > I also think that requiring full command names is a step back from
   > legacy Vim script.

We might still recommend full command names in the help; for 2 reasons:

   - consistency
   - easier refactoring

With regards to the second bullet point, suppose you want to apply a modifier like `:keepjumps` or `:keeppatterns` for every substitution in your (possibly huge) config/plugins.  Good luck finding all of them if you've used the short form `:s` with arbitrary pattern delimiters.  OTOH, looking for `substitute` is easy and will mostly give relevant results.

This kind of recommendation could be included in a new `:help vim9script-styleguide` help tag.

   > And the idea mentioned earlier
   > that shortening :global to "g" should require not being followed by
   > white space.

For consistency, the requirement should not be limited to the short form `:g`, but to all forms of the command, including `:global`.  Any pitfall affecting `g` also affects `global`; and considering that the latter will be more rarely used as a variable name is subjective.

Also, people might ask for more relaxed rules regarding whitespace (see here for a [real request](https://github.com/vim/vim/issues/7338)).  If that happens, then we might be able to write this kind of assignment:

    g+=a+b

At that point, the ambiguity with a global command would arise again.

## ?

    #!/bin/bash

    files=$(find . -type d -path './tmp' -prune -o -type f -name '*.vim' \
      | xargs grep -l '^vim9script' \
      | xargs grep -l '^\s*def\s')

    for file in $files; do
      vim -Nu NONE $file -S <(tee <<'EOF'
        set runtimepath^=~/.vim
        set runtimepath^=~/.vim/pack/mine/opt/lg-lib/
        set runtimepath^=~/.vim/pack/mine/opt/submode/
        call append('$', 'defcompile')
        silent! global/^\s*finish$/delete _
        update
        source %
    EOF
    )
    done

---

Write `:defcompile` at the end of any file matching this pattern:

    ^vim9script\_.*\n\s*enddef$

Then: for every match, run:

    :call append('$', 'defcompile') | update | exe 'norm! Gzv' | so%

Fix whatever errors you find in your code.
Report any bug you find in Vim.

Update: Wait until the recent patches  which implement type checking for builtin
functions stop.  There is no point  in making time-consuming tests now, if their
results change in a few days/weeks.

Update: If you get this kind of error:

    E1073: Name already defined: SomeFunc

Try to remove `noclear` after `:vim9script`.

## ?

<https://github.com/vim/vim/issues/8803>

I  think `:breakadd  expr` needs  a little  more documentation  and should  give
answers to these questions:

   - in `:breakadd expr {expression}`, is `{expression}` limited to a variable name?
   - are boolean numbers and booleans considered to be different values (i.e. is 0 the same as `v:false`)?
   - if `:breakadd expr {expression}` is written in a Vim9 script, is `{expression}` evaluated in the Vim9 context?

---
```vim
breakadd expr execute('ls!') =~ 'bar'
function Func()
    edit bar
    eval 1 + 0
endfunction
edit foo
call Func()
```
Why doesn't Vim stop when `Func()` edits `bar` causing the output of `ls!` to match `bar`?  Is it because the expression can only be a variable name?

---
```vim
vim9script
breakadd expr execute('ls') =~ 'file'
packadd netrw
Explore
```
The execution stops and Vim prints this:

    Oldval = "v:false"
    Newval = "0"

One might expect that `v:false` and `0` are handled like the same value.  Should/could they?  Or are we meant to turn booleans into numbers with `? 1 : 0`:

    breakadd expr execute('ls') =~ 'file' ? 1 : 0
                                          ^-----^

And the `v:` prefix in front of `v:false` suggests that the expression is evaluated in the legacy context (in Vim9, it would have been dropped, just like in `:vim9 echo v:false`).  But `:breakadd expr` is written in a Vim9 script. Shouldn't the expression be evaluated in the Vim9 context?

## ?

Sometimes, we have an error such as:

    E1013: Argument N: type mismatch, expected ... but got ...

Not enough context.  For which function call exactly?
This matters a lot if we have a  chain of method calls on a single line (because
then, the line number of the error cannot help).

Find an example.  Report the issue.

## ?

About pattern delimiters.

Should not cause any issue:

    ;
    ,
    `
    _


Might cause an issue because they can start a comment:

    "
    #

Might cause an issue because they are used in regex atoms:

    $
    .
    =
    ?
    @
    \
    ^

Might cause an issue because they are used as binary operators:

    +
    -
    *
    /
    %

Don't know:

    !
    &
    '
    |
    ~

    <
    >
    (
    )
    [
    ]
    {
    }

---

yl"_dd?patb"_xPE"_xP||/```\_s*\zs
yl"_dd?patB"_xPEE"_xP||/```\_s*\zs

```vim
s \pat\ rep
```

    ^
    +
    -
    *
    /
    %
    !
    &
    '
    |
    ~
    <
    >
    (
    )
    [
    ]
    {
    }

---

In Vim9:

    E476: Invalid command: filter |pat| ls
    E476: Invalid command: filter | pat | ls

    E476: Invalid command: filter # pat # ls

    E492: Not an editor command: filter _ pat _ ls

    E476: Invalid command: filter .pat. ls
    E476: Invalid command: filter . pat . ls

    E476: Invalid command: filter =pat= ls
    E476: Invalid command: filter = pat = ls

In legacy:

    E476: Invalid command: filter |pat| ls
    E476: Invalid command: filter | pat | ls

    E476: Invalid command: filter "pat" ls
    E476: Invalid command: filter " pat " ls

    E492: Not an editor command: filter _ pat _ ls

---

`!` is a special case.
In Vim9, it works in this case:
```vim
vim9script
filter ! pat! ls
```
    ✔

If there is no space after the first `!`, the command is invalid:
```vim
vim9script
filter !pat! ls
```
    E476: Invalid command: filter !pat! ls
```vim
vim9script
filter !pat ! ls
```
    E476: Invalid command: filter !pat ! ls

If there is a space after the first `!`, and also before the second `!`, what follows is executed as a shell command:
```vim
vim9script
filter ! pat ! echo 'shell command'
```
    shell command

In legacy, it works iff the second bang is not preceded by a space:
```vim
filter !pat! ls
```
    ✔
```vim
filter ! pat! ls
```
    ✔

If it is, again, what follows the second bang is executed as a shell command:
```vim
filter !pat ! echo 'shell command'
```
    shell command
```vim
filter ! pat ! echo 'shell command'
```
    shell command

---

According to `:h pattern-delimiter`, we can't use a double quote as a delimiter around a pattern passed as an argument to a command such as `:substitute` or `:global`:

> *pattern-delimiter* *E146*
> Instead of the '/' which surrounds the pattern and replacement string, you
> can use any other single-byte character, but not an alphanumeric character,
> '\', '"' or '|'.  This is useful if you want to include a '/' in the search
> pattern or replacement string.

In Vim9, that's still true:
```vim
vim9script
['aba bab']->repeat(3)->setline(1)
sil! s/nowhere//
:% s"b"B"g
```
    E486: Pattern not found: nowhere

Should it?  `"` is no longer a comment leader in Vim9.

Also, since `#` is the comment leader in Vim9, should it be disallowed in Vim9?
Right now, it works:
```vim
vim9script
['aba bab']->repeat(3)->setline(1)
sil! s/nowhere//
:% s#b#B#g
:% p
```
    aBa BaB
    aBa BaB
    aBa BaB

## ?

According to the help, these functions accept a funcref as an argument:

  - `:help call()`
  - `:help eval()`
  - `:help filter()`
  - `:help function()`
  - `:help map()`
  - `:help search()`
  - `:help searchpair()`
  - `:help setqflist()`
  - `:help sort()`
  - `:help substitute()`
  - `:help timer_start()`

Do they also accept a function name?
```vim
function Func()
    echo 'working'
endfunction
call call('Func', [])
```
    working
```vim
function Func()
    return 'working'
endfunction
echo 'Func'->string()->eval()()
```
    E15: Invalid expression: )
```vim
function MyFilter(i, v)
    return a:v =~ 'keep'
endfunction
echo ['removeme', 'keepme', 'deleteme']->filter('MyFilter')
```
    E121: Undefined variable: MyFilter
```vim
echo function('strlen')('working')
```
    7
```vim
function MyMap(i, v)
    return a:v * 100
endfunction
echo [1, 2, 3]->map('MyMap')
```
    E121: Undefined variable: MyMap
```vim
call setline(1, ['if', '" endif', 'endif'])
syntax on
set filetype=vim
function MySkip()
    return synstack('.', col('.'))
        \ ->map({_, v -> synIDattr(v, 'name')})
        \ ->match('\ccomment') != -1
endfunction
echo search('\<endif\>', '', 0, 0, 'MySkip')
```
    E121: Undefined variable: MySkip
```vim
call setline(1, ['if', '" endif', 'endif'])
syntax on
set filetype=vim
function MySkip()
    return synstack('.', col('.'))
        \ ->map({_, v -> synIDattr(v, 'name')})
        \ ->match('\ccomment') != -1
endfunction
echo searchpair('\<if\>', '', '\<endif\>', '', 'MySkip')
```
    E121: Undefined variable: MySkip
```vim
function Func(info)
    return repeat(['test'], 100)
endfunction
call setqflist([], 'r', {'lines': v:oldfiles, 'efm': '%f', 'quickfixtextfunc': 'Func'})
cwindow
```
    no error
```vim
function Func()
    echo ['bbb', 'aaa']->sort('MySort')
endfunction
function MySort(line1, line2)
    return a:line1 > a:line2 ? 1 : -1
endfunction
call Func()
```
    ['aaa', 'bbb']
```vim
function MyRep()
    return 1
endfunction
echo substitute('aaa', '.', MyRep, 'g')
```
    E121: Undefined variable: MyRep
```vim
function MyCb(_)
    echom 'my callback'
endfunction
call timer_start(0, 'MyCb')
```
    my callback

Conclusion:  Out of the 11 functions, 5 accept a function name instead of a funcref:

   - `call()`
   - `function()`
   - `setqflist()`
   - `sort()`
   - `timer_start()`

It would  not be possible for  the other 6  functions to accept a  function name
with quotes, because they already accept  arbitrary strings, and parse them in a
certain way.   For example,  `map()` accepts an  eval string  containing `v:val`
and/or `v:key`,  while `substitute()`  accepts a string  whose contents  is used
literally to replace a pattern.

You might wonder why that's an  issue; after all, `sort()` also accepts strings,
and yet,  it also accepts  function names.  That's  true, but `sort()`  does not
accept *arbitrary* strings.   Only a limited set of strings.   And out of those,
only  1 could  be ambiguous  (`'N'` is  parsed  as a  flag, while  it's a  valid
function name).

I think you should document this in our Vim notes.

## ?

When a function accepts a function name as an argument, how does it work in Vim9
script?  That is, does it still work *with* quotes?  Can it work *without* quotes?
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
def Strlen(str: string): number
    return strlen(str)
enddef
def Func()
    echo function('Strlen')('working')
enddef
Func()
```
    7
```vim
vim9script
def Strlen(str: string): number
    return strlen(str)
enddef
def Func()
    echo function(Strlen)('working')
enddef
Func()
```
    7
```vim
vim9script
def MyQftf(info: any): any
    return repeat(['test'], 100)
enddef
def Func()
    setqflist([], 'r', {'lines': v:oldfiles, 'efm': '%f', 'quickfixtextfunc': 'MyQftf'})
    cwindow
enddef
Func()
```
    no error
```vim
vim9script
def MyQftf(info: any): any
    return repeat(['test'], 100)
enddef
def Func()
    setqflist([], 'r', {'lines': v:oldfiles, 'efm': '%f', 'quickfixtextfunc': MyQftf})
    cwindow
enddef
Func()
```
    no error
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
    ['aaa', 'bbb']
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
def Strlen(str: string): number
    return strlen(str)
enddef
echo function('Strlen')('working')
```
    7
```vim
vim9script
def Strlen(str: string): number
    return strlen(str)
enddef
echo function(Strlen)('working')
```
    7
```vim
vim9script
def MyQftf(info: any): any
    return repeat(['test'], 100)
enddef
setqflist([], 'r', {'lines': v:oldfiles, 'efm': '%f', 'quickfixtextfunc': 'MyQftf'})
cwindow
```
    no error
```vim
vim9script
def MyQftf(info: any): any
    return repeat(['test'], 100)
enddef
setqflist([], 'r', {'lines': v:oldfiles, 'efm': '%f', 'quickfixtextfunc': MyQftf})
cwindow
```
    no error
```vim
vim9script
def MySort(line1: string, line2: string): number
    return line1 > line2 ? 1 : -1
enddef
echo ['bbb', 'aaa']->sort('MySort')
```
    ['aaa', 'bbb']
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

   - we can still use quotes
   - we can now also omit the quotes

You should document that the quotes can now be omitted in our Vim9 notes.
Also, it should be documented at `:h vim9`; I don't think it is.
There is  something at `:h vim9  /omitting function()`, but it's  about the fact
that we  can drop `function()`.  It  doesn't explicitly tell us  that the quotes
can be dropped.  Although, I guess it can be guessed from the example:

    var Funcref = MyFunction
                  ^--------^
                  no quotes

Still, I think it would be better if it was written explicitly.

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
    [function('<SNR>1_MyMap'), function('<SNR>1_MyMap'), function('<SNR>1_MyMap')]
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
        ->mapnew((_, v) => synIDattr(v, 'name'))
        ->match('\ccomment') != -1
enddef
def Func()
    echo search('\<endif\>', '', 0, 0, 'MySkip')
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
        ->mapnew((_, v) => synIDattr(v, 'name'))
        ->match('\ccomment') != -1
enddef
def Func()
    echo search('\<endif\>', '', 0, 0, MySkip)
enddef
Func()
```
    3
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
def MySkip(): bool
    return synstack('.', col('.'))
        ->mapnew((_, v) => synIDattr(v, 'name'))
        ->match('\ccomment') != -1
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
        ->mapnew((_, v) => synIDattr(v, 'name'))
        ->match('\ccomment') != -1
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
    [function('<SNR>1_MyMap'), function('<SNR>1_MyMap'), function('<SNR>1_MyMap')]
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
        ->mapnew((_, v) => synIDattr(v, 'name'))
        ->match('\ccomment') != -1
enddef
echo search('\<endif\>', '', 0, 0, 'MySkip')
```
    E703: Using a Funcref as a Number
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
def MySkip(): bool
    return synstack('.', col('.'))
        ->mapnew((_, v) => synIDattr(v, 'name'))
        ->match('\ccomment') != -1
enddef
echo search('\<endif\>', '', 0, 0, MySkip)
```
    3
```vim
vim9script
setline(1, ['if', '" endif', 'endif'])
syn on
set ft=vim
def MySkip(): bool
    return synstack('.', col('.'))
        ->mapnew((_, v) => synIDattr(v, 'name'))
        ->match('\ccomment') != -1
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
        ->mapnew((_, v) => synIDattr(v, 'name'))
        ->match('\ccomment') != -1
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

Conclusion:
We can now use a function name instead of a funcref, but only *without* quotes.
They don't  accept function  names with quotes,  for the same  reason as  in Vim
script legacy; they already accept strings, which they parse in a specific way.

To document in our notes (and at `:h vim9`?).

## ?

Did we miss some tests about `function()`?
Read what we wrote about `function()` in our Vim9 notes.

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

## Do we need `nr2float()`?
```vim
vim9script
var f: float
var n = 123
f = n
```
    E1012: Type mismatch; expected float but got number

Workaround:
```vim
vim9script
var f: float
var n = 123
f = n + 0.0
echo f
```
    123.0

Or:
```vim
vim9script
var f: float
var n = 123
f = n->string()->str2float()
echo f
```
    123.0

---

Python has `float()`: <https://www.w3schools.com/python/ref_func_float.asp>

## inconsistent and confusing format to separate context from errors in messages

Consider this snippet:
```vim
vim9script
var name = 0
lockvar name
name = 0
```
It correctly gives `E741`:

    E741: Value is locked: name

Notice how the context (here `name`) is separated from the cause of the error; with a colon:

    E741: Value is locked: name
                         ^

Now, consider this other snippet:
```vim
vim9script
v:count = 0
```
    E46: Cannot change read-only variable "v:count"

Notice that – this time – the context (`v:count`) is separated from the cause of the error with quotes:

    E46: Cannot change read-only variable "v:count"
                                          ^       ^

This is inconsistent.

Quotes are useful when an error contains an expression.
Without, if the expression is an empty string, the message gets confusing.

Are there other inconsistent error messages regarding the usage of quotes?

---
```vim
const NAME = 123
NAME = 1234
```
    E46: Cannot change read-only variable "NAME"
```vim
var NAME = 123
lockvar NAME
NAME = 1234
```
    E741: Value is locked: NAME

I think the format of the second error message is better.  That is, this:

    E1234: Some error: some context

is more readable than this:

    E1234: Some error "some context"

It might not  be obvious here, but  there are some error messages  in Vim9 which
use the second format, and you wonder whether the quotes are part of the context
(i.e. semantic) or just surrounding characters (i.e. syntaxic).
```vim
echo 'a'..'b'
```
    E1004: White space required before and after '..' at "..'b'"

This would be more readable:

    E1004: White space required before and after '..' at: ..'b'

This would also be more consistent with other error messages.
I think `E1004` is the only one which uses quotes to separate the context from the error.
I think all the other ones use a colon.

## ?
```vim
vim9script
var x = 3
var line = 'abcdef'
echo line[x:]
```
    E1004: White space required before and after ':' at ":]"
    ✔
```vim
vim9script
var s = 3
var line = 'abcdef'
echo line[s:]
```
    E731: using Dictionary as a String
    ✘

Same thing when `s` is replaced with `b`, `g`, `t`, `v`, `w`.

---
```vim
vim9script
var a = 3
var line = 'abcdef'
echo line[a:]
```
    E121: Undefined variable: a:

It should be:  "E1004: White space required before and after ':'".

Same thing when we replace `a` with `l`.

---
```vim
vim9script
def Func()
    var a = 3
    var line = 'abcdef'
    echo line[a:]
enddef
Func()
```
    E1075: Namespace not supported: a:]

It should be:  "E1004: White space required before and after ':'".

Same thing when `a` is replaced with any character, except `b`, `g`, `t`, `w`.

Here is a – maybe less-contrived – example:
```vim
vim9script
def Func()
    var mylist = [5, 4, 3, 2, 1]
    var v = 1
    var count = 3
    var otherlist = mylist[v: count]
    echo otherlist
enddef
Func()
```
    E1075: Namespace not supported: v: count]

This error message will probably look confusing to a new Vim user.
More generally, I suspect that `E1075` should never be given for a sublist.

## ?

Study these tests:

- <https://github.com/vim/vim/commit/65c4415276394c871c7a8711c7633c19ec9235b1#diff-38c87bcbc3bdd4cd44544298e1942ce03bcfece8fbead0d19f9c7abf592fcef4>
- <https://github.com/vim/vim/commit/9e68c32563d8c9ffe1ac04ecd4ccd730af66b97c#diff-38c87bcbc3bdd4cd44544298e1942ce03bcfece8fbead0d19f9c7abf592fcef4>
- <https://github.com/vim/vim/commit/7e3682068bebc53a5d1e9eaaba61bb4fa9c612da#diff-38c87bcbc3bdd4cd44544298e1942ce03bcfece8fbead0d19f9c7abf592fcef4>

Make sure you understand all the syntaxes they use.

## ?
```vim
vim9script
def Func()
    if exists('name')
        echo name
    endif
enddef
defcompile
```
    E1001: Variable not found: name
```vim
vim9script
def Func()
    if exists('g:name')
        echo g:name
    endif
enddef
defcompile
```
    no error
```vim
vim9script
if exists('name')
    echo name
endif
```
    no error

Why an error in the first snippet?

Workaround:
```vim
vim9script
def Func()
    if exists('name')
        echo name
    endif
enddef
var name: string
defcompile
```
    no error

Update: I  don't think  it's a  bug.   I think  you  should rarely  if ever  use
`exists()` (or `get()`) with a script-local  variable.

Indeed, if you check the existence of such a variable, you probably have written
some code which deletes it.  But that's not allowed in Vim9 script.

Instead of deleting a  variable, try to make it "empty"  (`''`, `[]`, `{}`, `0`,
...), or give it an invalid value.

Using an empty value  is especially convenient because it lets  you use the null
coalescing operator `??`.

## Vim9: cannot use the s: namespace in a :def function

**Describe the bug**

In Vim9 script, we cannot use the `s:` namespace in a `:def` function.

**To Reproduce**

Run this shell command:

    $ vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        def Func()
            echo s:
        enddef
        defcompile
    EOF
    )

`E1075` is given:

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

`E1075` is not documented in the help, but it is also given when we try to nest a script-local function inside another one:
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
It would help if it was supported to refactor future Vim script legacy functions
where we've written `get(s:, ...)` (we have a few dozens of those).

If it can't be made to work, maybe this limitation should be documented (`:h vim9-gotchas`).

Update:  I found a workaround which relies on the null coalescing operator.
```vim
" old code using get(s:, ...)
function Func()
    echo get(s:, 'name', 123)
endfunction
```
```vim
" new code using ??
vim9script
def Func()
    echo name ?? 123
enddef
var name: number
```
---

It might be documented at `:h :def`:

   > If the script the function is defined in is Vim9 script, then script-local
   > variables can be accessed without the "s:" prefix.  **They must be defined**
   > **before the function is compiled.**

But there's nothing  in there which says that we  cannot access the script-local
dictionary.

## imported constants and variables not added to the "s:" dictionary

    imported constant
```vim
vim9script
g:lines =<< trim END
    vim9script
    export const s:MYCONST = 123
END
mkdir('/tmp/import', 'p')
g:lines->writefile('/tmp/import/foo.vim')
set rtp+=/tmp
import 'foo.vim'
echo foo.MYCONST
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
    export var s:name = 123
END
g:lines->writefile('/tmp/import/foo.vim')
set rtp+=/tmp
import 'foo.vim'
echo foo.name
echo s:
echo get(s:, 'name', 456)
```
    123
    ✔
    {}
    ✘
    456
    ✘

## ?

The help says that curly braces names cannot be used in Vim9.
But what's the equivalent if we're refactoring a legacy script?
The closest thing I can  think of, is to use a dictionary:
```vim
vim9script
var d: dict<any>
def Func()
    var key = 'name'
    d[key] = 123
    echo d.name
enddef
Func()
```
    123

Here, our  value is not  stored in a  variable whose name  is dynamic, but  in a
dictionary whose key names are dynamic.

## Vim9: should Vim's help include its own Vim9 script style guide similar to `:help coding-style`?

Maybe it could be based on the one provided by Google.

## ?

Github needs to support proper syntax highlighting for Vim9 script:
<https://github.com/Alhadis/language-viml>

## Vim9: can still use legacy syntax script#var to declare autoload variables

**Steps to reproduce**

Run this shell command:

    $ vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        var dir = '/tmp/.vim'
        dir->delete('rf')
        &runtimepath = dir
        dir ..= '/plugin'
        dir->mkdir('p')
        var lines =<< trim END
            vim9script
            g:script#var = 123
        END
        lines->writefile(dir .. '/script.vim')
        source /tmp/.vim/plugin/script.vim
        echo script#var
    EOF
    )

No error is given.  `123` is echo'ed.

**Expected behavior**

An error is given.  Nothing is echo'ed.

Because:

   - allowing `script#var`, and at the same time disallowing `script#Func()` is confusing
   - it doesn't make sense to declare an autoload variable in a script under a `plugin/` directory; it should be inside an autoload script

Regarding the last bullet point, here is a confirmation that it's not a valid usage, even in legacy:

   > The system can be abused, yes.  But this is a side effect of how it was
   > implemented, and no effort was made to disallow it.  I think it would be
   > good to disallow it in Vim9 script, because it does look like abuse and
   > not valid usage.

Source: <https://github.com/vim/vim/issues/9637#issuecomment-1024688333>

Obviously, we can't disallow this invalid usage in legacy, it would break existing scripts.  But we can disallow it in Vim9, and enforce the `export` way of creating such variables.

**Version of Vim**

8.2 Included patches: 1-4386

**Environment**

Operating system: Ubuntu 20.04.3 LTS
Terminal: xterm
Value of $TERM: xterm-256color
Shell: zsh 5.8

**Additional context**

Same issue in an autoload script:
```vim
vim9script
var dir = '/tmp/.vim'
dir->delete('rf')
&runtimepath = dir
dir ..= '/autoload'
dir->mkdir('p')
var lines =<< trim END
    vim9script
    g:script#number = 123
    export def Func()
    enddef
END
lines->writefile(dir .. '/script.vim')
import autoload 'script.vim'
script.Func()
echo script#number
```
    123

Update: If we do this, won't we break this script?

    ~/.vim/plugin/sandwich.vim

Also, do we need to make a distinction between creating and referring to an autoload variable?
What about autoload function with the old syntax?
We can no longer define them, but do we have the guarantee that we can still call them in Vim9 script?

---

[We can omit the `g:` prefix](https://github.com/vim/vim/issues/6553) in front of the name of an autoload function in its header, and at any call site.

But we *cannot* omit `g:` for an autoload variable:
```vim
vim9script
var foo#bar = 123
```
    E461: Illegal variable name: foo#bar
```vim
vim9script
foo#bar = 123
```
    E492: Not an editor command:     foo#bar = 123
```vim
vim9script
g:foo#bar = 123
```
    no error

To document?

<https://github.com/vim/vim/issues/9637#issuecomment-1024486891>

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

---

`:help vim9` was correctly updated, but not `:help autoload`:
<https://github.com/vim/vim/issues/6553>

---

   > It's like these are exported to this autoload namespace.

If an autoload  function is really exported  to some namespace, does  it mean we
don't need to use the `export` command to export it?
And we  can automatically  import it  under whatever name  we want  from another
script?  Make some tests.

## ?
```vim
vim9script
def Func()
enddef
var d = {func: Func}
d.func(0)
```
    E118: Too many arguments for function: <SNR>1_Func
```vim
vim9script
def Func()
enddef
var d: dict<func> = {func: Func}
d.func(0)
```
    E118: Too many arguments for function: <SNR>1_Func
```vim
vim9script
def Func()
enddef
def Test()
    var d = {func: Func}
    d.func(0)
enddef
Test()
```
    E118: Too many arguments for function: d.func(0)

To be consistent, shouldn't the error message print `<SNR>1_Func` rather than `d.func(0)`?
Besides, `(0)` should not even be printed; it's not part of the function name...

## Vim9: should 'clipboard' and 'selection' be considered to be set with their default values

**Describe the bug**

In Vim9 script, should `'clipboard'` and `'selection'` be considered to be set with their default values when a script starts being sourced or a `:def` function starts being run?  Just like `'cpo'`:

https://github.com/vim/vim/blob/8f22f5c3aa0aa96e3843a57f29405625d8514c74/runtime/doc/vim9.txt#L879-L881

This would avoid issues which arise when we implement operators.

**To Reproduce**

Run this shell command:

    $ vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        # suppose this is set in the user's vimrc
        set cb=unnamedplus selection=exclusive

        # suppose this is a plugin
        nnoremap <expr> <F3> CountLetters()
        def CountLetters(type = ''): string
            if type == ''
                set opfunc=CountLetters
                return 'g@'
            endif
            var commands = {line: "'[V']y", char: "`[v`]y", block: "`[\<c-v>`]y"}
            exe 'norm! ' .. get(commands, type, '"')
            echom getreg('"')->strlen()
            return ''
        enddef
        setline(1, 'some text')
        @+ = ''
        feedkeys("\<F3>iw")
    EOF
    )

It echo'es 3, and the `"+` register has been altered.

**Expected behavior**

It echo'es 4, and the `"+` register has not been altered.

**Environment**

 - Vim version: 8.2 Included patches: 1-2165
 - OS: Ubuntu 16.04.7 LTS
 - Terminal: xterm(362)

**Additional context**

To avoid this pitfall, a plugin's author must take care of saving and restoring the options:
```vim
vim9script
set cb=unnamedplus selection=exclusive

nnoremap <expr> <F3> CountLetters()
def CountLetters(type = ''): string
    if type == ''
      set opfunc=CountLetters
      return 'g@'
    endif
    var selection_save = &selection
    var clipboard_save = &clipboard
    try
        set clipboard= selection=inclusive
        var commands = {line: "'[V']y", char: "`[v`]y", block: "`[\<c-v>`]y"}
        exe 'norm! ' .. get(commands, type, '"')
        echom getreg('"')->strlen()
    finally
        &clipboard = clipboard_save
        &selection = selection_save
    endtry
    return ''
enddef
setline(1, 'some text')
@+ = ''
feedkeys("\<F3>iw")
```
---

Although, I'm not sure it's possible or desireable.
There could be some overhead each time a function is invoked to reset and restore the options.

Besides, isn't this an example of more general issues?
When you implement a command (in particular an opfunc), you want:

   - the logic of your code to be immune from the user's settings
   - your code to have as fewer side-effects as possible (e.g. no register mutation)

Could Vim9 do sth to address these?
Or should we ask for helper functions?
Asan example, see `:h todo /option_save`.

Note that even with  the helper functions mentioned in this  todo item, it would
still  be a  lot of  work in  each opfunc.   You would  still need  to know  the
existence of these options, and that they might influence an opfunc.
You would  still need  to temporarily reset  them.  You would  still need  a try
conditional.

Would it make sense to ask for `'cb'` and `'sel'` to be temporarily reset *only*
in opfuncs?

### ?

What about:

   - `'isident'`
   - `'langremap'`
   - `'virtualedit'`

## ?

Do you remember our  trick which consists in using the wrong  type `job` to make
Vim give an error, and copy the right type from the message?
And, do you  remember that when the  message gives a composite  type with `any`,
like `dict<any>` or `list<any>`, we can never trust the `any` part?
So we have to first use sth wrong again, like `dict<job>` or `list<job>`...

Well, the  issue *could*  come –  at least  in part  – from  the fact  that some
builtin functions have a too generic return type.
See here for how this issue was fixed for `winsaveview()`:
<https://github.com/vim/vim/commit/43b69b39acb85a2aab2310cba5a2dbac338a4eb9>

Have a look at `~/VCS/vim/src/evalfunc.c` and look for this pattern:

    /ret_\S\+any

Check whether the return type of some functions could be made more accurate.
For example, I think that would be the case for:

   - `popup_getoptions()`
   - `searchcount()`

Send a patch.

## ?

This commit tried  to make it possible to  assign the output of a  function to a
boolean variable, if it can only return a boolean number:

<https://github.com/vim/vim/commit/3af15ab7888033fdfae0ae7085172aab794339a2>

Check it didn't omit any relevant function.

Also, try to write tests:

<https://github.com/vim/vim/issues/7693#issuecomment-761823852>

## ?

<https://github.com/vim/vim/issues/7759#issuecomment-770345327>

Make sure to also generate snippets to test builtin functions at the script level.

## ?

In a for loop, the iteration variable is locked:
```vim
vim9script
def Func()
    for i in [1, 2, 3]
        i = 4
    endfor
enddef
defcompile
```
    E1018: Cannot assign to a constant: i

Could we make an exception for when we assign a new value with the same type?
Otherwise, we have to create an extra variable which copies the iteration value.
See `vim-man`:

    # ~/.vim/pack/mine/opt/man/autoload/man.vim
    for char in Gmatch(line, '[^\d128-\d191][\d128-\d191]*')
        ...
        var c: string = char
        ^------------------^

This looks a bit awkward (the fact that `char` is written twice...).
Also, this locking doesn't exist in lua.
Does it exist in typescript?

---

Note that if  you iterate over a  list of dictionaries, you can  still make them
mutate:
```vim
vim9script
var l = [{key: 0}]
for d in l
    ++d.key
endfor
echo l
```
    [{'key': 1}]
             ^

## ?
```vim
vim9script
com Cmd eval 0
def Func()
    Cmd
enddef
disa Func
```
    <SNR>1_Func
        Cmd
       0 EXEC     Cmd
       1 RETURN 0

At compile time, should Vim expand a custom command and compile the result?

    <SNR>1_Func
        eval 0
       0 PUSHNR 0
       1 DROP
       2 RETURN 0

## ?
```vim
vim9script
g:.foo = 0
```
    E1069: White space required after ':': :.foo = 0

Weird error message...

I think it would be better to just say sth like "invalid variable name".

---

Note that this works since 8.2.4589:
```vim
vim9script
g:['foo'] = 0
echo g:foo
```
    0

## ?

Should we add help tags for the Vim9 "commands" `:{` and `:}`?

## ?
```vim
vim9script
{
    a: 1,
    b: 2
}->setline(1)
```
    E121: Undefined variable: a:

Confusing.  Could  Vim check whether  there is  a method call  afterward, before
parsing `{}` as a block?

Yes, it would be  an extra rule to implement, but the block  syntax is already a
corner case in itself (rarely useful); adding a rule on top of that would not be
a big deal, right?

## unexpected E1095 when unclosed string below :return
```vim
vim9script
def Func(): number
    if 1
        " wrong legacy comment
        return 0
    endif
    return 0
enddef
defcompile
```
    E114: Missing quote: " wrong legacy comment
```vim
vim9script
def Func(): number
    if 1
        return 0
        " wrong legacy comment
    endif
    return 0
enddef
defcompile
```
    E1095: Unreachable code after :return

It would be easier to fix the issue if `E114` was given in the second snippet.
It's  not really  a  bug; `"  wrong  ...`  is parsed  as  unclosed string  which
technically  is code  (remember that  a  string is  an expression,  and you  can
evaluate an expression without `:eval`).
Still,  could  Vim  first  check  for unclosed  strings  *before*  checking  for
unreachable code after a `:return`?

I guess not.  Worth asking?

##
##
## documentation
### 77

You can't use `.` for concatenation.

You must use `..`:

    $ vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        var str = 'a' . 'b'
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

### 180

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

### 363

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
+It is not allowed to assign a value to a register with `:var`. >
+	var @a = 'my register'		# Error!
+	@a = 'my register'		# OK
+	setreg('a', 'my register')	# OK
+
 							*E1092*
 Declaring more than one variable at a time, using the unpack notation, is
 currently not supported: >
```
### 411

> A method call without `eval` is possible, so long as the start is an
> identifier or can't be an Ex command.  **For a function either "(" or "->" must**
> **be following, without a line break.**  Examples: >

Not sure to understand.
Does it mean that a function name must be followed by a paren?
Or that alternatively, it must be followed by `->`?
(but in this case, it's not a function name; it's a funcref)

### 420

I would rewrite this whole paragraph:

> The boolean operators "||" and "&&" expect the values to be boolean, zero or
> one: >
>       1 || false   == true
>       0 || 1       == true
>       0 || false   == false
>       1 && true    == true
>       0 && 1       == false
>       8 || 0       Error!
>       'yes' && 0   Error!
>       [] || 99     Error!

into this:

> The boolean operators "||" and "&&" expect the values to be boolean, zero or
> one: >
>       1 || false   evaluates to true
>       0 || 1       evaluates to true
>       0 || false   evaluates to false
>       1 && true    evaluates to true
>       0 && 1       evaluates to false
>       8 || 0       Error!
>       'yes' && 0   Error!
>       [] || 99     Error!

Or into this:

> The boolean operators "||" and "&&" expect the values to be boolean, zero or
> one: >
>       (1 || false)   == true
>       (0 || 1)       == true
>       (0 || false)   == false
>       (1 && true)    == true
>       (0 && 1)       == false
>       8 || 0       Error!
>       'yes' && 0   Error!
>       [] || 99     Error!

It's less confusing.  Otherwise, you're tempted  to run the command as is, which
can give unexpected results.

For example:
```vim
vim9script
echo 0 || 1 == true
```
    E1072: Cannot compare number with bool
```vim
vim9script
echo (0 || 1) == true
```
    ✔

### 431

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

### 436

We can pass a function name to  functions which accept a funcref as an argument,
*without* quotes.

It's not documented.  There is this:

   > Omitting function() ~

   > A user defined function can be used as a function reference in an expression
   > without `function()`. The argument types and return type will then be checked.
   > The function must already have been defined. >

   >         var Funcref = MyFunction

   > When using `function()` the resulting type is "func", a function with any
   > number of arguments and any return type.  The function can be defined later.

But  it's about  the fact  that `function()`  *can* be  dropped, it  doesn't say
anything about the fact that the quotes *can* or *must* be dropped.  This should
be documented at `:h vim9-differences`.

<https://github.com/vim/vim/issues/6788>

### 731

   > Comparators ~
   >
   > The 'ignorecase' option is not used for comparators that use strings.

The help  should say something about  whether a comparison operator  matches the
case or ignore the case by default; that is, what happens if you don't prefix it
with `#` nor `?`.

Answer: it matches the case.

### 850

At `:h  vim9-gotchas`, I would add  a gotcha about  the fact that you  can *not*
omit `s:` when calling a script-local or imported function from a `:function` function.
It sounds obvious, but  in practice, I bet you might  sometimes forget and don't
understand why your code doesn't work.
```vim
vim9script
function Foo()
    call Bar()
endfunction
def Bar()
    echo 'bar'
enddef
Foo()
```
    E117: Unknown function: Bar

The reason why you might forget, is because  in Vim9 script you can omit `s:` in
front of a function name most of the time; that is when:

   - defining a `:def` function
   - defining a `:function` function
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

### 881

   > Vim9 functions are compiled as a whole: >
   >         def Maybe()
   >           if !has('feature')
   >             return
   >           endif
   >           use-feature  " May give compilation error
   >         enddef

I can reproduce this pitfall:
```vim
vim9script
def Func()
    if !has('sound')
        return
    endif
    sound_playfile('/usr/share/sounds/alsa/Rear_Right.wav')
enddef
defcompile
```
    E117: Unknown function: sound_playfile
    # this assumes that you compiled Vim without sound support

        ./configure --disable-canberra
                    ^----------------^

But why no error here?
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
In addition  to checking  whether a  function is  available, shouldn't  Vim also
check whether an Ex command is available?

Even simpler:
```vim
vim9script
def Func()
    ruby print('Hello')
enddef
defcompile
```
    no error

This doesn't give any error, even though my Vim doesn't support the ruby interface.
If this is  working as intended, maybe  we should better document  which kind of
syntax is checked for existence/availability  at compile time (e.g. functions vs
Ex commands).

---

   > For a workaround, split it in two functions: >
   >         func Maybe()
   >           if has('feature')
   >             call MaybeInner()
   >           endif
   >         endfunc
   >         if has('feature')
   >           def MaybeInner()
   >             use-feature
   >           enddef
   >         endif

The repetition of `has('feature')` looks awkward and is inefficient.
This is better:

    func Maybe()
      call MaybeInner()
    endfunc
    if has('feature')
      def MaybeInner()
        use-feature
      enddef
    else
      def MaybeInner()
      enddef
    endif

No more repetition,  and when you have `feature`, `Maybe()`  is not checking for
the existence  of `feature`  on every single  invocation, which  is inefficient;
especially if `Maybe()` is invoked frequently (e.g. `CursorMoved`).

### 985

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

### 1239

From `:h :vim9 /vim9-namespace/;/common`:

   > In Vim9 script the global "g:" namespace can still be used as before.  And the
   > "w:", "b:" and "t:" namespaces.  These have in common that variables are not
   > declared and they can be deleted.

Maybe environment variables should be mentioned as well.

And maybe registers (like `@r`).
Indeed, you can't use `:var` with them; but you can't you use `:unlet` either.

Also, I would rewrite the whole paragraph like this:

   > In Vim9 script the global "g:" namespace can still be used as before.  And the
   > "w:", "b:", "t:", and "$" namespaces.  These have in common that their
   > variables cannot be declared but can be deleted.
   > For variables which are local to a script, function or code block, the opposite
   > is true.  They can be declared but cannot be deleted.

### 1306

   > {not implemented yet: using "This as That"}

This line should be removed because `This as That` is available since 8.2.2556.

### 1328

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

    $ tee <<'EOF' /tmp/A.vim
        vim9script
        import '/tmp/B.vim'
        export const PI = 3.14159
    EOF

    $ tee <<'EOF' /tmp/B.vim
        vim9script
        import '/tmp/A.vim'
        echomsg A.PI
    EOF

    $ vim -Nu NONE -S /tmp/A.vim

    E1048: Item not found in script: PI˜

### 1456

   > The error can be given at compile time, no error handling is needed at runtime.

If  the function  contains a  type error,  it's still  installed (like  a legacy
function), but its body is empty.

This is neat, and maybe it should be documented.
If a  legacy function  contains syntax/type errors,  and was  invoked frequently
(e.g. `InsertCharPre`  autocmd), the  same errors  were given  repeatedly.  This
shoud not happen with a `:def` function.

But note that this is limited to an error which is found at compile time; not at
execution time.

### 1601

   > In Vim9 type checking is stricter to avoid mistakes.  Where a condition is
   > used, e.g. with the `:if` command **and the `||` operator**, only boolean-like
   > values are accepted:

I think it should be:

   > and the `?:` operator

`||` doesn't expect a condition; it expects expressions:

    echo 0 > 9 || 1
         ├───┘    │
         │        └ that's not a condition either
         └ that's not a condition

OTOH, the first argument of `?:` is indeed used as a condition.

### 1646

   > When sourcing a Vim9 script from a legacy script, only the items defined
   > globally can be used; not the exported items.

Actually, I think you can also use any item defined in the `b:`, `t:`, and `w:` namespace;
but not one defined in the `s:` namespace.

### ?

`++var` and `--var` should be replaced with `++name` and `--name`.
To avoid confusion with `:var`.

### ?

Something should be said about the new rule which disallows white space:

   - before a comma separating 2 items in a list or dictionary
   - before a colon separating 2 items in a dictionary

And about the new rule which enforces white space after a colon separating a key
from its value in a dictionary.

### ?

We can nest `:def` inside `:function`, but not the reverse.
```vim
vim9script
def Vim9()
    function Legacy()
    endfunction
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

### concept of block-local function

There is this at `:h vim9-declaration`:

   > The variables are only visible in the block where they are defined and nested
   > blocks.  Once the block ends the variable is no longer accessible: >

But it's about variables; there is nothing about functions.

##
# Todo list
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
# Popups
## ?
```vim
vim9script
&winminheight = 0
autocmd WinEnter * wincmd _
prop_type_add('textprop', {})
def Popup(text: string)
    text->setline(1)
    prop_add(1, 1, {type: 'textprop', bufnr: bufnr('%')})
    var col = text->strlen()
    popup_create(text, {textprop: 'textprop', col: col, border: []})
enddef
Popup('foo')
new
Popup('bar')
```
Expected: the `foo` popup is hidden.
Actual: it's weirdly squashed vertically on the left.

## cannot scroll to bottom of popup window using builtin popup filter menu when height equal to terminal window

<https://vi.stackexchange.com/questions/27320/scrolling-down-in-popup-window-not-working-as-intended>

As a workaround, you can use a custom filter:

    call range(50)
        \ ->map({_, i -> string(i)})
        \ ->popup_create(#{
        \ line: 1,
        \ col: 1,
        \ minwidth: 1,
        \ minheight: 1,
        \ cursorline: 1,
        \ wrap: 0,
        \ mapping: 0,
        \ filter: 'MyMenuFilter',
        \ firstline: 1,
        \ })

    function MyMenuFilter(id, key)
        if a:key == 'j'
            call win_execute(a:id, 'norm! j')
            call popup_setoptions(a:id, #{firstline: 0})
            return 1
        endif
        return popup_filter_menu(a:id, a:key)
    endfunction

It looks  like a bug.   If a custom  filter can make  Vim scroll a  popup window
whose height  is `&lines`,  the builtin filter  should be able  to do  the same.
Unless it's a design choice?  Is it documented?

## Improve `:help popup-examples /TODO`

   > TODO: more interesting examples

What about a mapping which allows to annotate?
Useful while reading the Vim user manual.
It could illustrate how to replicate the virtual text feature in Vim.
The example should  automatically create an editable copy of  a user manual page
(similar to vimtutor):

    :new | read $VIMRUNTIME/doc/usr_01.txt

If the  code gets too complex,  maybe we could  write a small package  (like for
`:Cfilter`) and submit a PR.

Update: It's an interesting idea, but not for virtual text.
An annotation might be too long for an end of line.

I have another idea: a command which adds virtual text based on the qf list.

    vim9script
    helpgrep foobar
    def Func()
        var qfl = getqflist()
        var i = 1
        for entry in qfl
            prop_type_add('markendofline' .. i, {})
            prop_add(entry.lnum, col([entry.lnum, '$']), {type: 'markendofline' .. i})
            popup_create(entry.text, {
                textprop: 'markendofline' .. i,
                highlight: 'ErrorMsg',
                line: -1,
                col: 2,
                zindex: 49,
                })
            i += 1
        endfor
    enddef
    Func()

## ?

    $ vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        set lines=24
        var opts = {
            line: 13,
            minheight: 10,
            maxheight: 10,
            border: [],
            }
        popup_create(['aaa', 'bbb', 'ccc'], opts)
    EOF
    )

Notice how the bottom of the popup reaches the bottom of the terminal window.
Now, let's increment `line` by 1:

    $ vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        set lines=24
        var opts = {
            line: 14,
            minheight: 10,
            maxheight: 10,
            border: [],
            }
        popup_create(['aaa', 'bbb', 'ccc'], opts)
    EOF
    )

Notice how the popup unexpectedly starts from the top of the terminal window.
Is it documented or is it a bug?

##
# Misc.
## confusing error when running `:packadd` while `'debug'` set to `throw`.

    $ vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        &runtimepath = ''
        &debug = 'throw'
        &packpath = '/tmp/issue'
        (&packpath .. '/pack/mine/opt/foobar')->mkdir('p')
        packadd foobar
    EOF
    )

    E121: Undefined variable: g:did_load_filetypes

I think the error is given because of this line:

    // file: src/scriptfile.c, line 778
    char_u *cmd = vim_strsave((char_u *)"g:did_load_filetypes");

Because it persists  even if you remove all  occurrences of `did_load_filetypes`
from the runtime files.

---

The issue is not specific to Vim9.

---

It might not be a bug.  But maybe document this somewhere.

## ?

Ask for  `autocmd_add()` to support a  lambda/funcref (and a `{}`  block?) to be
supported when specifying the value of the `cmd` key.

<https://github.com/vim/vim/pull/10291#issuecomment-1109905203>

## ?

    You have two options for customizing a color scheme.  For changing the
    appearance of specific colors, you can redefine a color name before loading
    the scheme.  The desert scheme uses the khaki color for the cursor.  To use a
    darker variation of the same color: >

            let v:colornames['khaki'] = '#bdb76b'
            colorscheme desert

Doesn't work.

    $ vim --clean
    :colorscheme desert
    :put =execute('highlight Cursor')
    Cursor         xxx guifg=#333333 guibg=#f0e68c

    $ vim --clean
    :let v:colornames['khaki'] = '#bdb76b'
    :colorscheme desert
    :put =execute('highlight Cursor')
    Cursor         xxx guifg=#333333 guibg=#f0e68c

## ?

    :echo getcompletion('debug ', 'cmdline')

Actual:

    []

Expected:

    [list of Ex command names]

---

    :echo getcompletion('debug call ', 'cmdline')

Actual:

    []

Expected:

    [list of function names]

---

Same issue if we replace `:debug` with any other modifier.

## ?

    # open an xterm terminal
    vim -Nu NONE -S <(tee <<'EOF'
        vim9script
        &showcmd = true
        nnoremap <C-W>> <C-W>>
    EOF
    )
    # press <C-W>

Actual: This is printed on the right of the last line of the screen:

    <80>ü^DW

Expected: This is printed on the right of the last line of the screen:

    ^W

The issue disappear if we clear `'t_TI'` and `'t_TE'`:

    &t_TI = ''
    &t_TE = ''

Didn't we already report this issue in the past?

If  it's working  as intended  (i.e.  the showcmd  area  is meant  to print  the
internal byte representation of the keys, not the keys themselves), it should be
documented.  Is it?

## ?

   - <https://github.com/vim/vim/issues/9240#issuecomment-981605560>
   - <https://github.com/vim/vim/issues/9240#issuecomment-981626034>

---
```vim
vim9script
def Func()
    eval 01 + 0
    eval 02 + 0
    eval 03 + 0
    eval 04 + 0
    eval 05 + 0
    eval 06 + 0
    eval 07 + 0
    eval 08 + 0
    eval 09 + 0
    eval 10 + 0
    eval 11 + 0
    eval 12 + 0
enddef
for i in range(1, 12)
    execute 'breakadd func ' .. i .. ' Func'
endfor
breakdel 1'2
filter /line 12/ breaklist
```
    12  func Func  line 12
    ✘
    everything was ignored after the quote
    same issue with :center, :copy (and :t), :digraphs

---
```vim
vim9script
for i in range(1, 12)
    execute 'edit file' .. i
endfor
buffer 1'2
```
    E94: No matching buffer for 1'2
    same result with :bunload, :bwipeout, :diffget, :diffput

Update: Now I think it's documented at `:help :buffer`:

   > The notation with single quotes does not work here,
   > `:buf 12'345'` uses 12'345 as a buffer name.

---
```vim
vim9script
for i in range(1, 12)
    execute 'edit file' .. i
endfor
caddbuffer 1'2
```
    E474: Invalid argument
    same result with :cbuffer, :cgetbuffer

---
```vim
vim9script
silent helpgrep foobar
clist 1'2, 34
```
    E488: Trailing characters: '2, 34

---
```vim
vim9script
&define = '#define'
'#define FOO'->setline(1)
'FOO'->setline(2)
:2
djump 0'1 /FOO/
```
    E388: Couldn't find definition

---

    :help :djump
    :help :dsearch
    :help :dsplit
    :help :earlier
    :help :goto
    :help :ijump
    :help :isearch
    :help :isplit
    :help :laddbuffer
    :help :later
    :help :lbuffer
    :help :left
    :help :lfirst
    :help :lgetbuffer
    :help :list
    :help :ll
    :help :llast
    :help :llist
    :help :lnewer
    :help :loadview
    :help :lolder
    :help :lopen
    :help :lrewind
    :help :lwindow
    :help :move
    :help :number
    :help :previous
    :help :psearch
    :help :resize
    :help :retab
    :help :right
    :help :sNext
    :help :sall
    :help :sargument
    :help :sbNext
    :help :sball
    :help :sbmodified
    :help :sbnext
    :help :sbprevious
    :help :sbuffer
    :help :sleep
    :help :sprevious
    :help :substitute
    :help :sunhide
    :help :tabmove
    :help :tabnext
    :help :tabonly
    :help :tabprevious
    :help :undo
    :help :unhide
    :help :winpos
    :help :winsize
    :help :z

## 'verbose' message not printed until scroll back and forth

**Steps to reproduce**

Run this shell command:

    $ vim -Nu NONE -i NONE +'4verbose echo system("seq " .. 2*&lines)'

The output of `seq(1)` is printed in Vim's pager: this is expected.
The first line of Vim's pager is empty: this is NOT expected.

**Expected behavior**

The first line of Vim's pager prints the exact shell command which Vim has run to get the output of `system()`.  Something like:

    Calling shell to execute: "(seq 123)>/tmp/vsZS9Kf/0 2>&1"

**Operating system**

Ubuntu 20.04.3 LTS

**Version of Vim**

8.2 Included patches: 1-3656

**Screenshot**

![gif](https://user-images.githubusercontent.com/8505073/143058325-9e982a48-2d00-4beb-8f28-91fa45360202.gif)

In the previous screenshot, we can see that the first line is initially empty.  Then, after scrolling back and forth by pressing `j` then `k`, the "Calling shell to execute: ..." message is finally printed.  It would be less confusing if it was printed immediately, without us having to scroll.

---

There are other issues.  Sometimes, some lines in the output of `system()` are blank.
It depends on the number of lines:

    vim -Nu NONE -i NONE +'4verbose echo system("seq " .. 2*&lines)'
                                                          ^------^
                                                          make more tests, and play with that number

## Possibly stale items at `:help todo /Vim script language`:

    8   Make the filename and line number available to script functions, so that
        they can give useful debugging info.  The whole call stack would be ideal.
        At least use this for error messages.

`:echo expand('<stack>')`

---

    7   Pre-parse or compile Vim scripts into a bytecode.
        1. Put the bytecode with the original script, with an ":if
           has('bytecode')" around it, so that it's only used with a Vim that
           supports it.  Update the code with a command, can be used in an
           autocommand.
        2. Use a ".vic" file (like Python use .pyc).  Create it when writing a
           .vim file.  Problem: distribution.
        3. Use a cache directory for each user.  How to recognize which cached
           file belongs to a sourced script?

`:def`

---

    7   Add argument to winwidth() to subtract the space taken by 'foldcolumn',
        signs and/or 'number'.

`:echo win_getid()->getwininfo()[0].textoff`

---

    6   Add ++ and -- operators?  They only work on variables (lvals), how to
        implement this?

Vim9

---

    8   argc() returns 0 when using "vim -t tag".  How to detect that no file was
        specified in any way?  To be able to jump to the last edited file.

`v:argv`???

---

    8   Pass the command line arguments to Vim scripts in some way.  As v:args
        List?  Or extra parameter to argv()?

`v:argv`

---

   -   Replace ccomplete.vim by cppcomplete.vim from www.vim.org?  script 1520 by
       Vissale Neang.  (Martin Stubenschrott) Asked Vissale to make the scripts
       more friendly for the Vim distribution.
       New version received 2008 Jan 6.
       No maintenance in two years...

The "new" version should be 13 years old now.
No update on vim.org.

## ?

Study these plugins (rather short and interesting/useful):

- <https://github.com/bfrg/vim-fzy>
- <https://github.com/bfrg/vim-qf-diagnostics>
- <https://github.com/habamax/vim-minisnip>

## ?

<https://github.com/vim/vim/issues/1246>

> I'm willing to try to diagnose it further, just need some general guidance

Install the netrw plugin as an optional package.  For example, under `~/.vim/pack/mine/opt/netrw/`.

The file hierarchy should look like this:

    .
    ├── autoload
    │   ├── netrwFileHandlers.vim
    │   ├── netrw_gitignore.vim
    │   ├── netrwSettings.vim
    │   └── netrw.vim
    ├── doc
    │   └── pi_netrw.txt
    ├── plugin
    │   └── netrwPlugin.vim
    ├── syntax
    │   └── netrw.vim
    └── tags

    4 directories, 8 files

Now, you need a minimal vimrc which reproduces the issue.  As an incomplete start:
```vim
vim9script
g:netrw_altfile = 1
packadd netrw
Explore
```
Start Vim like with this shell command:

    vim -Nu /tmp/vimrc
            ^--------^
            path to your minimal vimrc

There is a hit-enter prompt.  Use `:silent` to get rid of it:
```vim
vim9script
g:netrw_altfile = 1
packadd netrw
silent Explore
```
Now, automate the `file1` search:
```vim
vim9script
g:netrw_altfile = 1
packadd netrw
silent Explore
search('file1')
```
It fails.  You probably need to delay the search via a one-shot autocmd:
```vim
vim9script
g:netrw_altfile = 1
packadd netrw
silent Explore
autocmd VimEnter * ++once Delay()
def Delay()
    search('file1')
enddef
```
It works.  Now, use `feedkeys()` to automate the `Enter` keypress:
```vim
vim9script
g:netrw_altfile = 1
packadd netrw
silent Explore
autocmd VimEnter * ++once Delay()
def Delay()
    search('file1')
    feedkeys("\<Enter>", 't')
enddef
```
Now, automate the second `:Explore`:
```vim
vim9script
g:netrw_altfile = 1
packadd netrw
silent Explore
autocmd VimEnter * ++once Delay()
def Delay()
    search('file1')
    feedkeys("\<Enter>", 't')
    Explore
enddef
```
It fails.  Again, you probably need to delay the command via a one-shot autocmd:
```vim
vim9script
g:netrw_altfile = 1
packadd netrw
silent Explore
autocmd VimEnter * ++once Delay()
def Delay()
    search('file1')
    feedkeys("\<Enter>", 't')
    autocmd BufWinEnter * ++once Explore
enddef
```
For your first issue, you don't need to automate more than that.  Because if you execute `:ls!` right after the second `:Explore`, you should already notice an issue in the scenario 1:

    1u%a-  "~"                          line 123
    2      "file1"                      line 123

Notice that `file1` is not prefixed with the `%` nor with the `#` indicator.  IOW, there is no way to get it back with `C-^`.

Now, you need to add a breakpoint right before the second `:Explore` with `:breakadd`.  The latter only accepts function names, not command names.  So, you need the name of a function.  Ask Vim what is the name of the function which is called by `:Explore`:

    :command Explore
    !|  Explore           *    0c ?    dir         call netrw#Explore(<count>,0,0+<bang>0,<q-args>)
                                                        ^-----------^

The answer is `netrw#Explore()`.  You can add a breakpoint at its start like this:

    breakadd func 1 netrw#Explore

Your minimal vimrc should look like this:
```vim
vim9script
g:netrw_altfile = 1
packadd netrw
silent Explore
autocmd VimEnter * ++once Delay()
def Delay()
    search('file1')
    feedkeys("\<Enter>", 't')
    breakadd func 1 netrw#Explore
    autocmd BufWinEnter * ++once Explore
enddef
```
When you start Vim, the execution should stop right before executing the first command in the `netrw#Explore()` function:

    Breakpoint in "netrw#Explore" line 1
    Entering Debug mode.  Type "cont" to continue.
    function <SNR>3_NetrwBrowseChgDir[193]..BufWinEnter Autocommands for "*"..function netrw#Explore
    line 3: if !exists("b:netrw_curdir")

Run `ls!`; you should see something like this:

    1u h-  "~"                            line 107
    2 %a   "~/file1"                      line 1

`file1` has the `%` indicator, which is good; it means that Vim still remembers it, and that we should be able to retrieve later with `C-^`.

Now, execute the first line of the function, by typing `next` then press `Enter` (`next` can be shortened into `n`).
Ask again for a listing with `ls!`:

    1u h-  "~"                            line 107
    2 %a   "~/file1"                      line 1

`file1` still has the `%` indicator.  So far, so good.

Continue to execute `next`.  Don't bother running `ls!` after every `next`; only if the function has executed a command which might change the current file.  So, forget about control flow statements like `:if`, and forget about `:let` assignments.  Don't bother typing `next` or `n` every time; if your last command was `next`/`n` (and not `ls!`), then you can simply press `Enter`.

Eventually, you should see that the current file changes after a call to the `netrw#LocalBrowseCheck()` function:

    >
    function <SNR>3_NetrwBrowseChgDir[193]..BufWinEnter Autocommands for "*"..function netrw#Explore
    line 221: call netrw#LocalBrowseCheck(dirname)
    >ls!
      1u h-  "~"                            line 107
      2 %a   "~/file1"                      line 1

After the function has been called, it's too late to step into it:

   - quit Vim by executing `qa!`
   - edit your minimal vimrc to update the breakpoint:

         # before
         breakadd func 1 netrw#Explore
         # after
         breakadd func 1 netrw#LocalBrowseCheck

   - restart Vim

You should get this message at the start:

    Breakpoint in "netrw#LocalBrowseCheck" line 1
    Entering Debug mode.  Type "cont" to continue.
    function <SNR>3_NetrwBrowseChgDir[193]..BufWinEnter Autocommands for "*"..function netrw#Explore[221]..netrw#LocalBrows
    eCheck
    line 19: let ykeep= @@
    >ls!
      1u h-  "~"                            line 107
      2 %a   "~/file1"                      line 1

Update: `:breakadd expr` would make the process much simpler.

## ?
```vim
legacy let name = [] + + []
```
    E745: Using a List as a Number

Confusing message.

Update: It probably comes from this:
```vim
legacy let name = + []
```
    E745: Using a List as a Number

## ?

Refactor all  the help files  to encourage people to  use a more  up-to-date Vim
script syntax.  Here is non-exhaustive list:

   - . (concat operator) → ..
   - -> (methods)
   - optarg = 123 (get rid of "...", and a:0, a:1, ...)
   - full Ex command names
   - full option names
   - <Cmd>
   - non-recursive mappings

First, get a list of all the examples in the help files.
Those are highlighted by this syntax item:

    syn region helpExample      matchgroup=helpIgnore start=" >$" start="^>$" end="^[^ \t]"me=e-1 end="^<" concealends

So use this command to find their start:

    :Vim / >$\|^>$/gj $VIMRUNTIME/doc/**/*.txt

Review the list.
Whenever you find something wrong, note your position in the qfl.
Then fix the issue in all the examples.
Then, get back to your original position, and resume your review.
Create a dedicated branch in your Vim fork.

Finally, submit a PR.

## ?

This bug has probably been fixed in upstream:
<https://github.com/vim/vim/issues/6943>

See here:
<https://github.com/rohieb/vim/commit/a753912aa762dbd87fff4720eb8d76f0e8c46222>

But it hasn't been merged in Vim yet.
When it's done, leave a comment on #6943.

---

This bug has probably been fixed in upstream:
<https://github.com/vim/vim/issues/6777>

See here:
<https://github.com/tpope/vim-markdown/commit/276524ed9c8aec415d3c6dbeec7c05fbd31c95ce>

But it hasn't been merged in Vim yet.
When it's done, leave a comment on #6777.

## searchcount() can make Vim lag when the buffer contains a very long line
```vim
vim9script
@/ = 'x'
['x']
    ->repeat(1'000)
    ->map((_, v: string) => v .. repeat('_', 99))
    ->reduce((a: string, v: string) => a .. v)
    ->setline(1)
nnoremap <expr> n Func()
def Func(): string
    searchcount({maxcount: 1'000, timeout: 500})
    return 'n'
enddef
```
Keep pressing n for a few seconds, then stop: Vim still needs several seconds to
process the keypresses.

---

Note that the issue is not merely caused by the size of the buffer or the number
of matches.  Here is the exact same text, but splitted on 1000 lines:
```vim
vim9script
@/ = 'x'
repeat(['x'], 1000)
    ->map((_, v) => v .. repeat('_', 99))
    ->setline(1)
nnoremap <expr> n Func()
def Func(): string
    searchcount({maxcount: 1000, timeout: 500})
    return 'n'
enddef
set nu
```
Notice how this time, keeping `n` pressed doesn't cause Vim to lag.

Why does it matter for `searchcount()` whether a line is long or not?
Splitting short  lines into a single  long one doesn't change  the overall text,
nor the statistics about the search pattern...

---

Also note that the  number of matches must be high enough.   For example, in the
previous snippet, if we reduce the number  of matches from 1000 down to 500, Vim
lags a little less:
```vim
vim9script
@/ = 'x'
repeat(['x'], 500)
    ->map((_, v) => v .. repeat('_', 199))
    ->reduce((a, v) => a .. v)
    ->setline(1)
nnoremap <expr> n Func()
def Func(): string
    searchcount({maxcount: 1000, timeout: 500})
    return 'n'
enddef
```
Reduced further from 500 down to 250, it lags even less:
```vim
vim9script
@/ = 'x'
repeat(['x'], 250)
    ->map((_, v) => v .. repeat('_', 399))
    ->reduce((a, v) => a .. v)
    ->setline(1)
nnoremap <expr> n Func()
def Func(): string
    searchcount({maxcount: 1000, timeout: 500})
    return 'n'
enddef
```
And from 250 down to 125, the lag can no longer be perceived:
```vim
vim9script
@/ = 'x'
repeat(['x'], 125)
    ->map((_, v) => v .. repeat('_', 799))
    ->reduce((a, v) => a .. v)
    ->setline(1)
nnoremap <expr> n Func()
def Func(): string
    searchcount({maxcount: 1000, timeout: 500})
    return 'n'
enddef
```
---

You can't just refactor  `search#index()` so that it bails out  when you're on a
long line.  *Any* long line (even before or after) can make Vim lag.

---

<https://github.com/vim/vim/pull/4446#issuecomment-702825238>

##
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

## abbreviation sometimes unexpectedly expanded inside a word

**Describe the bug**

An abbreviation is sometimes unexpectedly expanded in the middle of a word.

**To Reproduce**

Run this shell command:

    $ vim -Nu NONE -S <(tee <<'EOF'
        set backspace=start
        inoreabbrev ab cd
        put! ='yyyy'
        normal! 3|
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

    augroup RestrictAbbreviations | autocmd!
        autocmd InsertEnter * start_insertion = {lnum: line('.'), col: col('.')}
        autocmd InsertCharPre * RestrictAbbreviations()
    augroup END
    var start_insertion: dict<number>
    def RestrictAbbreviations()
        var curlnum: number = line('.')
        if v:char =~ '\k'
            || start_insertion.col - 1 <= searchpos('[^[:keyword:]]', 'bn', curlnum)[1]
            || curlnum != start_insertion.lnum
            || state() =~ 'm'
            return
        endif
        feedkeys("\<C-V>" .. v:char)
        v:char = ''
    enddef

So far, it seems to work.
