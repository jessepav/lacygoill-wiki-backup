<https://github.com/vim/vim/blob/master/runtime/doc/vim9.txt>
<https://github.com/vim/vim/blob/master/runtime/doc/todo.txt>

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
## can delete a function-local or block-local function nested in a legacy function

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
    no error

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
var lines =<< trim END
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

### Add more functions to reduce the need to ":exe" commands with dynamic arguments

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

### Mappings

Mapping commands  could automatically add  `<sid>` in  front of a  function name
when it can't be found in the global namespace, but can in the script-local one.

---

Unfortunately, we  can't we  ask for mapping  commands to  automatically replace
`s:` with `<SID>`:

    :s/\C\<s:/<SID>/g

That would require Vim to parse the rhs which can be arbitrarily complex:

    nno <F3> <cmd>echo 'aaa s: bbb'<cr>
                            ^^
                            this should not be replaced with <SID>

Idea:  In the mappings table, could Vim store some kind of metadata, which would
include the ID of the script from where each mapping has been installed?

Before:

    :map
    ...˜
    n  <key>    * <Cmd>call <SNR>123_func()<CR>˜
    ...˜

After:

    :map
    ...˜
    n  <key>    * <Cmd>call <SID>func()<CR>˜
        SID = 123˜
    ...˜

---

This excerpt from `:h <SID>` looks wrong:

   > When defining a function in a script, "s:" can be prepended to the name to
   > make it local to the script.  But when a mapping is executed from outside of
   > the script, it doesn't know in which script the function was defined.  To
   > avoid this problem, use "<SID>" instead of "s:".  The same translation is done
   > as for mappings.  This makes it possible to define a call to the function in
   > a mapping.

It seems that it says that you need to prepend a function name with `<SID>` – at
the definition site –  if you want to call it from a  mapping.  That's not true.
Was it true in the past?

---

Mapping commands could interpret a bar as part of their argument.

---

A bar at the  start of a line could be parsed as  an automatic continuation line
when it follows a mapping command.

---

A local mapping could use `<nowait>` by default.

---

Vim could stop writing an automatic range when `:` is pressed from a normal mode
mapping.  This forces us to constantly write `:<c-u>`.

If the user wants a visual range, they should write it explicitly:

    xnoremap <F3> :*call Func()<CR>
                   ^

    xnoremap <F3> :'<,'>call Func()<CR>
                   ^---^

If the range is implicit, it leads to unexpected results for new users.

Although, it would be tricky to implement.
Vim would  probably have  to automatically  add `<c-u>` after  a colon;  but how
would it know which colons?
Idea: a mapping installed from a Vim9 script could be run in the Vim9 context.
And when a mapping is run in the Vim9 context, Vim would never automatically add
a range.

---

Inline comments could be disallowed in mappings:

    nno cd :echo 'foo'<cr> " some comment
                           ^------------^
                                 ✘

    nno ci :echo 'bar'<cr> # some comment
                           ^------------^
                                 ✘

Although, how Vim would know it's an inline comment?
*I remember people having issues because of inline comments; find an example of such issues.*

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
    E1107: String, List, Dict or Blob required

So, we'll have to use `? '': ''`, which looks cumbersome.

---

Btw, why is the error different at the script level?
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

    $ vim -Nu NONE -S <(cat <<'EOF'
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

    $ vim -Nu <(cat <<'EOF'
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

    $ vim -Nu NONE -S <(cat <<'EOF'
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

    $ vim -Nu NONE -S <(cat <<'EOF'
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

    $ vim -Nu NONE -S <(cat <<'EOF'
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

    $ vim -Nu NONE -S <(cat <<'EOF'
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

    $ vim -Nu NONE -S <(cat <<'EOF'
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

    $ vim -Nu <(cat <<'EOF'
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

No error is raised, but `E117` should be raised if the function was local to the
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

    $ vim -Nu NONE -S <(cat <<'EOF'
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

I think a different error should be raised.  Maybe `E1143`?
```vim
vim9script

def Func()
    eval # some comment
enddef
defcompile
```
    E1143: Empty expression: "# some comment"
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
    eval 1
    eval 2
    eval 3
enddef
def Func()
    eval 1
    eval 2
    eval 3
enddef
```
    Error detected while processing command line..script /proc/55113/fd/17:
    line   11:
    E1073: Name already defined: <SNR>1_Func

The error should be raised from line 7, not line 11; i.e. from the header rather
than from the footer.

### ?
```vim
vim9script
timer_start(1'000, (_) => 0)
exe 'verb ' .. timer_info()[0].callback
    ->string()
    ->substitute("('\\|')", ' ', 'g')
```
    function <lambda>1(...)
         Last set from /proc/26385/fd/11 line 1
    1  return 0
    endfunction

The line number of the definition is off by 1.
The lambda was not defined on line 1, but on line 2.
The issue is not specific to Vim9:
```vim
vim9script
eval 1
eval 2
eval 3
legacy let Ref = {-> 0}
verb function <lambda>1
```
        function <lambda>1(...)
             Last set from /proc/26909/fd/11 line 4
     1  return 0
        endfunction

Here, `:verb` tells us that the lambda was defined on line 4, which is wrong; it
was defined on line 5.

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
Func()
```
    Error detected while processing command line..script /proc/42151/fd/17:
    line    2:
    E1171: Missing } after inline function

Maybe the error should be raised from the function, rather than from the script.
Unless the error prevents Vim from finding `:enddef`...
But even then, it would help if the line address was closer to the issue (6 or 8).

### ?
```vim
vim9script
writefile(['compiler shellcheck'], '/tmp/t.vim')
silent edit /tmp/t.vim
source %
verbose set makeprg?
```
    makeprg=shellcheck -f gcc
          Last set from /tmp/t.vim line 18

It should print:

    makeprg=shellcheck -f gcc
          Last set from /usr/local/share/vim/vim82/compiler/shellcheck.vim line 18

Or:

    makeprg=shellcheck -f gcc
          Last set from /tmp/t.vim line 1

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
I'm not sure that can be done though; it seems Vim concatenates all the lines in
the lambda's definition:

    :fu <lambda>1
        def <lambda>1(m: any, ...): string˜
     1  return m[0]->str2nr() > 99                         ? ''                         : m[0]->str2nr()˜
        enddef˜

If it can't be  improved when the error is raised at runtime,  could it still be
improved when the error is raised at compile time?
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

##
## Vim9: "?:" operator can suppress error at compile time

**Describe the bug**

In Vim9 script, the `?:` operator can suppress an error at compile time.

**To Reproduce**

Run this shell command:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            [{k: 1}, {k: 2}]
                ->sort((a: dict<float>, b: dict<float>): number => a.k > b.k ? a.k - b.k : 0)
        enddef
        defcompile
    EOF
    )

No error is raised.

**Expected behavior**

`E1013` is raised:

    E1013: Argument 1: type mismatch, expected dict<float> but got dict<number>

**Environment**

 - Vim version: 8.2 Included patches: 1-3189
 - OS: Ubuntu 20.04.2 LTS
 - Terminal: XTerm(353)

**Additional context**

If `?:` is removed, an error is correctly raised at compile time:
```vim
vim9script
def Func()
    [{k: 1}, {k: 2}]
        ->sort((a: dict<float>, b: dict<float>): number => a.k - b.k)
enddef
defcompile
```
    E1012: Type mismatch; expected number but got float

Although, this error is about the return type, not the arguments type.

---

I think the issue comes from the fact that the first expression passed to the `?:` operator can't be tested at compile time.  That is, Vim doesn't know whether `a.k` is bigger than `b.k` at compile time.  And if it's false, then the expression evaluates to 0 which is a number whose type is valid.  Therefore, there is a *possibility* that the type is correct.

Still, shouldn't Vim be more strict by inspecting the type of *both* values at compile time, to make sure that all of them respect the return type specified for the lambda?

    a.k > b.k ? a.k - b.k : 0
                ^-------^   ^
                value 1     value 2

---

The issue disappears when we get rid of `sort()`:
```vim
vim9script
def Func()
    ((a: dict<float>, b: dict<float>): number => a.k > b.k ? a.k - b.k : 0)({k: 1}, {k: 2})
enddef
defcompile
```
    E1013: Argument 1: type mismatch, expected dict<float> but got dict<number>

Also, while the  argument type is sometimes checked at  compile time, the return
type never seems to be:
```vim
vim9script
def Func()
    ((d): dict<float> => d)({k: 1})
enddef
defcompile
```
    no error
```vim
vim9script
def Func()
    ((d: dict<float>) => d)({k: 1})
enddef
defcompile
```
    E1013: Argument 1: type mismatch, expected dict<float> but got dict<number>

### Is it the same issue?
```vim
vim9script
def Func()
    var n: number = 0
    var s: string = n != 0 ? n : ''
enddef
Func()
```
    no error
```vim
vim9script
def Func()
    var n: number = 1
    var s: string = n != 0 ? n : ''
enddef
Func()
```
    E1012: Type mismatch; expected string but got number

I think an error should be raised in the first snippet at compile time.

## ?

<https://github.com/vim/vim/issues/8776#issuecomment-906800314>

## ?

<https://github.com/vim/vim/issues/8719#issuecomment-894173355>

## ?

`term_getjob()` can return a job or a special.
But we cannot compare a job with a special.

This make some refactoring difficult.
For example, in `$VIMRUNTIME/pack/dist/opt/termdebug/plugin/termdebug.vim`:

    if gdbproc == v:null || job_status(gdbproc) !=# 'run'

In Vim9, we need to write:

    if gdbproc->typename() == 'special' && gdbproc == null
      || job_status(gdbproc) != 'run'

Should we allow the comparison between a job and a special?

Update: A better solution would be a comparison operator which ignores the type,
and only cares about the value.

## ?
```vim
vim9script
def Func()
    var s: list<string>
    s = [0]->map((_, v) => '')
enddef
defcompile
```
    E1012: Type mismatch; expected list<string> but got list<number>

The issue is in the `s` assignment; not in `map()`.
But it's not obvious.
Could we get more info?

    E1012: Type mismatch; expected string but got number in "s" assignment

## ?
```vim
vim9script
try
    var name = 123
finally
    echo name
endtry
```
    123
```vim
vim9script
def Func()
    try
        var name = 123
    finally
        echo name
    endtry
enddef
defcompile
```
    E1001: Variable not found: name

Inconsistent?

Update: Not really.  There is no real block scope at the script level.
It's emulated with a  script-local variable, which is deleted at  the end of the
block.  So, no inconsistency, right?

## ?

Sometimes, we have an error such as:

    E1013: Argument N: type mismatch, expected ... but got ...

Not enough context.  For which function call exactly?
This matters a lot if we have a  chain of method calls on a single line (because
then, the line number of the error cannot help).

Find an example.  Report the issue.

## ?
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

## ?

Check whether `typename()` returns a good signature for all builtin functions.

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

    E476: Invalid command: filter #pat# ls
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

##
## ?
```vim
vim9script
def Func()
    ['a', 'b', 'c']->map((_, v) => {
        echo v
    })
enddef
Func()
```
    a
    Error detected while processing command line..script /proc/37313/fd/17[7]..function <SNR>1_Func:
    line    3:
    E1012: Type mismatch; expected string but got void in map()

Why is `a` echo'ed?
Why is the error raised at runtime, and not earlier at compile time?
```vim
vim9script
def Func()
    ['']->map((_, v) => 0)
enddef
defcompile
```
    no error

##
## ?

"`=expr`" is not expanded in enough contexts
```vim
vim9script
def Func()
    var name = '/tmp/file'
    windo e `=name`
enddef
Func()
```
    E121: Undefined variable: name

---

In a global command, a backtick expansion works:
```vim
vim9script
def Func()
    var name = '/tmp/file'
    g/^/e `=name`
enddef
Func()
```
    no error

Same thing in a `:v` command:
```vim
vim9script
def Func()
    var name = '/tmp/file'
    v/not found/e `=name`
enddef
Func()
```
    no error

And in a `:folddoopen` command:
```vim
vim9script
def Func()
    var name = '/tmp/file'
    folddoopen e `=name`
enddef
Func()
```
    no error

And in a `:folddoclosed` command:
```vim
vim9script
def Func()
    var name = '/tmp/file'
    folddoclosed e `=name`
enddef
Func()
```
    no error

This seems inconsistent.  I think a backtick expansion should work in – at least
– all the frequently used commands/functions which execute other Ex commands.

That is `:bufdo`:
```vim
vim9script
def Func()
    var name = '/tmp/file'
    bufdo e `=name`
enddef
Func()
```
    E121: Undefined variable: name

`:argdo`:
```vim
vim9script
def Func()
    var name = '/tmp/file'
    args /tmp/file
    argdo e `=name`
enddef
Func()
```
    E121: Undefined variable: name

`:cdo`:
```vim
vim9script
def Func()
    var name = '/tmp/file'
    sil helpg grail
    cdo e `=name`
enddef
Func()
```
    E121: Undefined variable: name

`:cfdo`:
```vim
vim9script
def Func()
    var name = '/tmp/file'
    sil helpg grail
    cfdo e `=name`
enddef
Func()
```
    E121: Undefined variable: name

`:ldo`:
```vim
vim9script
def Func()
    var name = '/tmp/file'
    sil lh grail
    ldo e `=name`
enddef
Func()
```
    E121: Undefined variable: name

`:lfdo`:
```vim
vim9script
def Func()
    var name = '/tmp/file'
    sil lh grail
    lfdo e `=name`
enddef
Func()
```
    E121: Undefined variable: name

`execute()`:
```vim
vim9script
def Func()
    var name = '/tmp/file'
    execute('e `=name`')
enddef
Func()
```
    E121: Undefined variable: name

`win_execute()`:
```vim
vim9script
def Func()
    var name = '/tmp/file'
    win_execute(win_getid(), 'e `=name`')
enddef
Func()
```
    E121: Undefined variable: name

---

Also, it  is not clear  whether "`=expr`" is intended  to be expanded  for *any*
command,  including  ones  which  expect  an expression  as  an  argument  (like
`:echo`), or only for commands which expect a filename (like `:edit`).

The help suggests that it's intended for more than just commands expecting a filename:

   > The same is true for commands that are not compiled, such as `:global`.
   > For these the backtick expansion can be used.  Example: >
   >         def Replace()
   >           var newText = 'blah'
   >           g/pattern/s/^/`=newText`/
   >         enddef

But this seems to contradict this comment:

   > I don't think `=expr` is evaluated for an :echo command.

Source: <https://github.com/vim/vim/issues/7621#issuecomment-754800855>

And this other comment:

    // TODO: should only expand when appropriate for the command

Source: <https://github.com/vim/vim/blob/9ce47ec0b65f81358febacbd9b808ac8ef7af85c/src/vim9compile.c#L8434>

I think it  should be limited to  commands which expect a  filename as argument,
because:

   - it's consistent with legacy Vim script, where "`=expr`" only works for
     commands expecting a filename

   - it only seems to work with simple types; not with lists, dictionaries, functions:

```vim
vim9script
def Func()
    var d: dict<number>
    g/^/echo `=d`
enddef
defcompile
```
    E1105: Cannot convert dict to string

   - I think people will find it's a weird syntax anyway

Instead, maybe the  help should explain that  when an Ex command  is executed by
another command/function:

   - it's never compiled, therefore it can't access items in compiled code, like
     function-local variables

   - it's always run in the script context, therefore it *can* access any item
     in that namespace

   - if it needs to refer to an item, the latter should be in a "public"
     namespace (public = accessible by any script, like `g:`, `b:`, `w:`, ...),
     or in the script namespace

See also: <https://github.com/vim/vim/issues/7621#issuecomment-755085800>

## ?

According to the help, these functions accept a funcref as an argument:

  - `:h call()`
  - `:h eval()`
  - `:h filter()`
  - `:h function()`
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
echo function('strlen')('working')
```
    7
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
echo search('\<endif\>', '', 0, 0, 'MySkip')
```
    E121: Undefined variable: MySkip
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
```vim
fu Func(info)
    return repeat(['test'], 100)
endfu
call setqflist([], 'r', {'lines': v:oldfiles, 'efm': '%f', 'quickfixtextfunc': 'Func'})
cw
```
    no error
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
    cw
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
    cw
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
cw
```
    no error
```vim
vim9script
def MyQftf(info: any): any
    return repeat(['test'], 100)
enddef
setqflist([], 'r', {'lines': v:oldfiles, 'efm': '%f', 'quickfixtextfunc': MyQftf})
cw
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

## ?
```vim
vim9script

def FuncWithForwardCall()
    var Funcref = function('DefinedLater')
    echo Funcref
enddef

def DefinedLater()
enddef

FuncWithForwardCall()
```
    DefinedLater
```vim
vim9script

def FuncWithForwardCall()
    var Funcref = DefinedLater
    echo Funcref
enddef

def DefinedLater()
enddef

FuncWithForwardCall()
```
    <80><fd>R1_DefinedLater
    ^---------^
        bug?

##
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

## unexpected error when omitting type in variable declaration (probably not a bug)
```vim
vim9script
def Func()
    var x = getqflist()->map((_, v) => v.text->matchstr('.*'))
    var y = x[0]
    echo y[:]
enddef
defcompile
```
    E719: Cannot slice a Dictionary

There is indeed an error in the code, but not this one.
The error  occurred earlier:  `map()` changes the  type of  `getloclist(0)` from
`list<dict<any>>` to `list<string>`.

Similar issue here:
```vim
vim9script
def Func()
    for key in (range(char2nr('a'), char2nr('z'))
            + range(char2nr('A'), char2nr('Z')))
        ->map((_, v) => nr2char(v))
        toupper(key) == key
    endfor
enddef
Func()
```
    E1072: Cannot compare string with number

There is indeed an error in the code, but not this one.
The  error occurred  earlier:  `map()`  changes the  type  of `range(...)`  from
`list<number>` to `list<string>`.

Update: I don't think it can be fixed.
I think  these issues are  raised at compile time,  while the `map()`  error can
only be raised later, at runtime.

---

Wait.  Why no error here:
```vim
vim9script
def Func()
    [1, 2, 3]->map((_, v: float) => 0)
enddef
defcompile
```
## ?
```vim
vim9script
def Func()
    getbufinfo()
        ->map((_, v): dict<float> => v)
enddef
Func()
```
    E1012: Type mismatch; expected dict<float> but got dict<any>

This is expected.
(Although, why not at compile time? <https://github.com/vim/vim/issues/8092>)
```vim
vim9script
def Func()
    getbufinfo()
        ->sort((a: dict<float>, b: dict<float>) => 0)
enddef
Func()
```
    no error

Shouldn't Vim raise an error, just like in the previous snippet?
We're telling `sort()`  that it should receive dictionaries of  *floats*, but in
reality, we  pass it `getbufinfo()`  which outputs  a list of  dictionaries with
*mixed* values:

    :echo getbufinfo()->typename()
    list<dict<any>>˜

---
```vim
vim9script
def Func()
    getbufinfo()
        ->map((_, v): dict<number> => ({k: 0}))
        ->sort((a: dict<float>, b: dict<float>) => 0)
enddef
Func()
```
    no error

Shouldn't Vim raise an error?
In `map()`, we've declared that the list was transformed into a list of dictionaries of *numbers*.
But in `sort()`, we declare that it should expect a list of dictionaries of *floats*.
Those declarations are contradictory.  And yet Vim does not complain.  Why?

## ?
```vim
vim9script
def Func()
    var tags: list<dict<any>> = [{kind: 'a'}, {key: 123}, {kind: 'm'}]
    echo tags->filter((_, v: job) => v->has_key('kind') ? v.kind != 'm' : true)
enddef
defcompile
```
    E715: Dictionary required
```vim
vim9script
def Func()
    var tags: list<dict<any>> = [{kind: 'a'}, {key: 123}, {kind: 'm'}]
    echo tags->filter((_, v: dict<job>) => v->has_key('kind') ? v.kind != 'm' : true)
enddef
defcompile
```
    E1072: Cannot compare job with string

Why doesn't type checking warn us about the wrong type in the second argument of
the lambda?

Hypothesis:  Vim first  checks that the declared type of  the lambda's arguments
is compatible  with the expression  on the right of  `=>`. Later, it  will check
whether those types are compatible with what the filtered expression.

But this hypothesis is wrong:
```vim
vim9script
def Func()
    var tags: list<dict<any>> = [{kind: 'a'}, {key: 123}, {kind: 'm'}]
    echo tags->filter((_, v: job) => !v)
enddef
defcompile
```
    no error

##
## ?
```vim
vim9script
def Func()
    lockvar unknown
enddef
Func()
```
    no error

Should we give an error?

## ?
```vim
vim9script
append(-1, 'text')
```
    no error

Shouldn't an error be raised?  Like one of these:

    E1174: Positive number required for argument 1
    E1174: Positive number or String required for argument 1

---
```vim
vim9script
append('.aa', 'text')
```
    "text" is appended
```vim
vim9script
append('a.a', 'text')
```
    E1209: Invalid value for a line number: "a.a"

Same issue with `setline()`.
Only valid strings should be accepted.
Test all builtin functions which accept a string with a special meaning as argument.

Also, check how builtin functions handle invalid numbers.
For example, a negative number is invalid for `append()`.

##
## ?
```vim
vim9script
g:name = 123
echo name
```
    E121: Undefined variable: name

Shouldn't Vim look in the global namespace even without `g:`?
It's not a regression.

Note that Vim does look in the global namespace for a function:
```vim
vim9script
def g:Func()
    echo 'test'
enddef
Func()
```
    test

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

##
## ?
```vim
vim9 exe 'var x = 0'
```
    E1124: ":var" cannot be used in legacy Vim script

It would be nice if it worked.
This way, we could apply a single `:vim9` to multiple commands:
```vim
vim9 execute(['var l = range(5)', 'l->filter((_, v) => v % 2)'])
```
    E1124: ":var" cannot be used in legacy Vim script
    E488: Trailing characters: ->filter((_, v) => v % 2): l->filter((_, v) => v % 2)

Although, having to nest the statements inside strings is awkward...

In any case, if it's working as intended, should the help at `:h vim9` and/or at
`:h :exe` document  this limitation?  That is, should it  say that `:exe` always
executes a command in the legacy  context, regardless of whether it was prefixed
with `:vim9`?

## ?
```vim
vim9script
var s = 3
var line = 'abcdef'
echo line[s:]
```
    E731: using Dictionary as a String

Why "String"?
It should be:  "E123: using Dictionary as a Number".

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
More generally, I suspect that `E1075` should never be raised for a sublist.

## ?

Study these tests:

- <https://github.com/vim/vim/commit/65c4415276394c871c7a8711c7633c19ec9235b1#diff-38c87bcbc3bdd4cd44544298e1942ce03bcfece8fbead0d19f9c7abf592fcef4>
- <https://github.com/vim/vim/commit/9e68c32563d8c9ffe1ac04ecd4ccd730af66b97c#diff-38c87bcbc3bdd4cd44544298e1942ce03bcfece8fbead0d19f9c7abf592fcef4>
- <https://github.com/vim/vim/commit/7e3682068bebc53a5d1e9eaaba61bb4fa9c612da#diff-38c87bcbc3bdd4cd44544298e1942ce03bcfece8fbead0d19f9c7abf592fcef4>

Make sure you understand all the syntaxes they use.

##
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

## ?

Source this:

    vim9script
    def g:A()
    enddef
    A()

It works.
Now, remove `g:` in front of `A()`:

    def g:A()
    →
    def A()

And source the script a second time.
It still works.
Now, add `g:` back (undo), and source again:

    E117: Unknown function: A

Why?

It seems the  last time we sourced  the script, the script-local  `A()` has been
removed.  I  guess that  right before  sourcing a script,  Vim first  clears the
script-local namespace.
But what is weird is that Vim does not look in the global namespace anymore.
Why?

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
It would help if it was supported to refactor future Vim script legacy functions
where we've written `get(s:, ...)` (we have a few dozens of those).

If it can't be made to work, maybe this limitation should be documented (`:h vim9-gotchas`).

Update:  I found a workaround which relies on the null coalescing operator.
```vim
" old code using get(s:, ...)
fu Func()
    echo get(s:, 'name', 123)
endfu
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
    export var s:var = 123
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

##
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
    E1191: Call to function that failed to compile: <SNR>1_A
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

Why isn't `E1191` raised in the second snippet?
The code is identical; the only difference is that `A()` has been renamed into `B()`.
Same results if you rename `Map()` into `Func()`.

##
## ?

By default, a function is local to the current script, right?

Does that remain true for:

   - `function('Func')`
   - `:breakadd func Func`
   - `:prof func Func`
   ...

If not, is this a bug?

## Vim9: should Vim's help include its own Vim9 script style guide similar to `:h coding-style`?

Maybe it could be based on the one provided by Google.

## ?

How to get proper syntax highlighting for Vim9 code on github?

   1. <https://stackoverflow.com/a/8886392/9780968>
   2. <https://github.com/github/linguist/issues/1874#issuecomment-66876794>
   3. <https://github.com/SalGnt/Sublime-VimL>

## ?

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

`:h vim9` was correctly updated, but not `:h autoload`:
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
```vim
vim9script
def Func()
enddef
def Test()
    var d: dict<func> = {func: Func}
    d.func(0)
enddef
Test()
```
    E118: Too many arguments for function: <80><fd>R1_Func

The byte sequence `<80><fd>R` in the last error message looks weird.

## Vim9: should 'clipboard' and 'selection' be considered to be set with their default values

**Describe the bug**

In Vim9 script, should `'clipboard'` and `'selection'` be considered to be set with their default values when a script starts being sourced or a `:def` function starts being run?  Just like `'cpo'`:

https://github.com/vim/vim/blob/8f22f5c3aa0aa96e3843a57f29405625d8514c74/runtime/doc/vim9.txt#L879-L881

This would avoid issues which arise when we implement operators.

**To Reproduce**

Run this shell command:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        # suppose this is set in the user's vimrc
        set cb=unnamedplus selection=exclusive

        # suppose this is a plugin
        nno <expr> <F3> CountLetters()
        def g:CountLetters(type = ''): string
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

nno <expr> <F3> CountLetters()
def g:CountLetters(type = ''): string
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

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func(n: number)
            return Func(n) .. ''
        enddef
        defcompile
    EOF
    )

    E1105: Cannot convert void to string

This error message comes  from the fact that `Func()` is has  no return type, in
which case Vim assumes the special  type "void".  So, `Func(n)` returns a "void"
value, but needs to be converted to a string to be concatenated with `''`.
But that's impossible, hence the error.

So, this error is correct; but it's still confusing.
For the programmer,  it would be easier  to fix the issue if  `E1096` was raised
instead; just like here:
```vim
vim9script
def Func(n: number)
    return ''
enddef
defcompile
```
    E1096: Returning a value in a function without a return type

I guess it would require that Vim re-orders the checks.
First, it should check whether the  function returns some value while the header
does not specify any return type.  Then, it should check the rest.

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

Have a look at `~/Vcs/vim/src/evalfunc.c` and look for this pattern:

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
```vim
vim9script
var l = [1, 2, 3]
l->map(4)
echo l
```
    [4, 4, 4]

An error  should be  raised because  the second  argument of  `map()` must  be a
string or a funcref; not a number.

---
```vim
vim9script
var l = [1, 2, 3]
l->filter(4)
echo l
```
    [1, 2, 3]

An error should  be raised because the  second argument of `filter()`  must be a
string or a funcref; not a number.

---

Is it related to this todo item?

   > - Check many more builtin function arguments at compile time.

## ?
```vim
var name = 0
lockvar name
name = 0
```
    E741: Value is locked: s:name
```vim
v:count = 0
```
    E46: Cannot change read-only variable "v:count"

Notice that there are no quotes in the first error message.
But then, there *are* quotes in the second one.
Inconsistent.
Which would be better?  I think no quotes...
Update: Although, quotes are are useful when an error contains an expression.
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

`ctags(1)` does not generate any tag for variables declared with `:var`.

Send a patch which refactors this line:

    // $HOME/Vcs/ctags/parsers/vim.c
    else if (wordMatchLen (line, "let", 3))

Into this line:

    else if (wordMatchLen (line, "let", 3) || wordMatchLen (line, "var", 3))

Do the same for `:final`?

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

    // $HOME/Vcs/ctags/parsers/vim.c
    parseVariableOrConstant()

Watch the derek banas playlist on C  to have just enough knowledge to understand
the code and refactor it.

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
def Func()
    var l = range(3)
    lockvar l
enddef
defcompile
```
    E1178: Cannot lock or unlock a local variable
```vim
vim9script
def Func()
    var l = range(3)
    lockvar 1 l
enddef
defcompile
```
    E488: Trailing characters: 1 l

Maybe the second snippet should raise the same error as the first one.

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
def Func(): number
    try
        return 1
    catch
        return 2
    endtry
enddef
defcompile
```
    E1027: Missing return statement

Why?

Compare:
```vim
vim9script
def Func(): number
    if rand() % 2
        return 1
    else
        return 2
    endif
enddef
defcompile
```
    no error

## ?
```vim
vim9script
g:.foo = 0
```
    E1010: Type not recognized: .foo = 0
```vim
vim9script
g:['foo'] = 0
```
    E1010: Type not recognized: ['foo'] = 0

Weird error message...

I think it would be better to just say sth like "invalid variable name".

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

## ?
```vim
vim9script
var d = {
    a-b: 123
}
echo d.a-b
```
    E716: Key not present in Dictionary: "a-b"

The `a-b` key *is* in the dictionary.
A less misleading error message would be:

    E1234: .key notation can only include digits, letters and underscores

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

It would be easier to fix the issue if `E114` was raised in the second snippet.
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

    $ vim -Nu NONE -S <(cat <<'EOF'
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

### 345

   > Global functions must be prefixed with "g:" when defining them, but can be
   > called without "g:".
   >         vim9script
   >         def g:GlobalFunc(): string
   >           return 'text'
   >         enddef
   >         echo GlobalFunc()

I would argue that it would be better for Vim to require `g:` when calling a function.
This would be consistent with variables, and this would make the code more readable.
In fact, it's even recommended a little earlier:

   > When referring to a function and no "s:" or "g:" prefix is used, Vim will
   > search for the function:
   > - in the function scope, in block scopes
   > - in the script scope, possibly imported
   > - in the list of global functions
   > **However, it is recommended to always use "g:" to refer to a global function**
   > **for clarity.**

Anyway, I think the recommendation should be written in the previous excerpt too.

   > Global functions must be prefixed with "g:" when defining them, but can be
   > called without "g:".
   >         vim9script
   >         def g:GlobalFunc(): string
   >           return 'text'
   >         enddef
   >         echo GlobalFunc()
   > **However, it is recommended to always use "g:" to refer to a global function**
   > **for clarity.**

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
omit `s:` when calling a script-local or imported function from a `:fu` function.
It sounds obvious, but  in practice, I bet you might  sometimes forget and don't
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

The reason why you might forget, is because  in Vim9 script you can omit `s:` in
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

### 881

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
   >             call MaybeInner()
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

    E1048: Item not found in script: BAR˜

### 1456

   > The error can be given at compile time, no error handling is needed at runtime.

If  the function  contains a  type error,  it's still  installed (like  a legacy
function), but its body is empty.

This is neat, and maybe it should be documented.
If a  legacy function  contains syntax/type errors,  and was  invoked frequently
(e.g. `InsertCharPre` autocmd),  the same  errors were raised  repeatedly.  This
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
## cannot hide popup attached to text property
```vim
vim9script
setline(1, 'some text')
prop_type_add('textprop', {})
prop_add(1, 9, {type: 'textprop', length: 5})
var id = popup_create('attached to "text"', {
    textprop: 'textprop',
    highlight: 'ErrorMsg',
    line: -1,
    })
popup_hide(id)
```

## Improve `:h popup-examples /TODO`

   > TODO: more interesting examples

What about a mapping which allows to annotate?
Useful while reading the Vim user manual.
It could illustrate how to replicate the virtual text feature in Vim.
The example should  automatically create an editable copy of  a user manual page
(similar to vimtutor):

    new | r $VIMRUNTIME/doc/usr_01.txt

If the  code gets too complex,  maybe we could  write a small package  (like for
`:Cfilter`) and submit a PR.

Update: It's an interesting idea, but not for virtual text.
An annotation might be too long for an end of line.

I have another idea: a command which adds virtual text based on the qf list.

    vim9script
    helpg foobar
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

    $ vim -Nu NONE -S <(cat <<'EOF'
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

    $ vim -Nu NONE -S <(cat <<'EOF'
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

## ?

Stale todo item:

   > -   Replace ccomplete.vim by cppcomplete.vim from www.vim.org?  script 1520 by
   >     Vissale Neang.  (Martin Stubenschrott) Asked Vissale to make the scripts
   >     more friendly for the Vim distribution.
   >     New version received 2008 Jan 6.
   >     No maintenance in two years...

The "new" version should be 13 years old now.
No update on vim.org.

## ?

From `:h matchlist()`:

   > Can also be used as a |method|: >
   >         GetList()->matchlist('word')

`GetList()` should be replaced with `GetText()`.

## ?

    $ cd /tmp && MANPAGER='vim -Nu NONE +"set wildignorecase" -' man man
    :find *
    # press Tab

    expected: * is replaced with some text (the first directory in `/usr/include`)
    actual:   * is not replaced

## ?

Matchparen issue:

    $ vim -Nu NORC -S <(cat <<'EOF'
        vim9script
        set breakindent
        set linebreak breakat+=]
        (repeat('x', 70) .. ']' .. repeat('x', 50) .. '[xxx]' .. repeat('x', 70))->setline(1)
        norm! 4e
    EOF
    )

Notice that the empty cells at the end of the second line are all highlighted.
The default matchparen plugin has the same issue.

---

MWE which does not depend on matchparen, and relies on a text property:
```vim
vim9script
set breakindent
set linebreak breakat+=]
(repeat('x', 70) .. ']' .. repeat('x', 50) .. '[xxx]' .. repeat('x', 70))->setline(1)
norm! 6e
prop_type_add('test', {highlight: 'ErrorMsg'})
prop_add(1, 126, {length: 1, type: 'test'})
```
MWE which does not depend on matchparen, and relies on a match:
```vim
vim9script
set breakindent
set linebreak breakat+=]
(repeat('x', 70) .. ']' .. repeat('x', 50) .. '[xxx]' .. repeat('x', 70))->setline(1)
norm! 6e
matchaddpos('ErrorMsg', [[1, 126]], 10, 3)
```
## ?

When we set `'debug'` to `throw`, no error is thrown if the expression evaluated
by `'foldtext'` is buggy.  It would help if it did.

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

    vim9script
    @/ = 'x'
    repeat(['x'], 1000)
        ->map((_, v) => v .. repeat('_', 99))
        ->reduce((a, v) => a .. v)
        ->setline(1)
    nno <expr> n Func()
    def g:Func(): string
        searchcount({maxcount: 1000, timeout: 500})
        return 'n'
    enddef

Keep pressing n for a few seconds, then stop: Vim still needs several seconds to
process the keypresses.

---

Note that the issue is not merely caused by the size of the buffer or the number
of matches.  Here is the exact same text, but splitted on 1000 lines:

    vim9script
    @/ = 'x'
    repeat(['x'], 1000)
        ->map((_, v) => v .. repeat('_', 99))
        ->setline(1)
    nno <expr> n Func()
    def g:Func(): string
        searchcount({maxcount: 1000, timeout: 500})
        return 'n'
    enddef
    set nu

Notice how this time, keeping `n` pressed doesn't cause Vim to lag.

Why does it matter for `searchcount()` whether a line is long or not?
Splitting short lines  into a single long one doesn't  change change the overall
text, nor the statistics about the search pattern...

---

Also note that the  number of matches must be high enough.   For example, in the
previous snippet, if we reduce the number  of matches from 1000 down to 500, Vim
lags a little less:

    vim9script
    @/ = 'x'
    repeat(['x'], 500)
        ->map((_, v) => v .. repeat('_', 199))
        ->reduce((a, v) => a .. v)
        ->setline(1)
    nno <expr> n Func()
    def g:Func(): string
        searchcount({maxcount: 1000, timeout: 500})
        return 'n'
    enddef

Reduced further from 500 down to 250, it lags even less:

    vim9script
    @/ = 'x'
    repeat(['x'], 250)
        ->map((_, v) => v .. repeat('_', 399))
        ->reduce((a, v) => a .. v)
        ->setline(1)
    nno <expr> n Func()
    def g:Func(): string
        searchcount({maxcount: 1000, timeout: 500})
        return 'n'
    enddef

And from 250 down to 125, the lag can no longer be perceived:

    vim9script
    @/ = 'x'
    repeat(['x'], 125)
        ->map((_, v) => v .. repeat('_', 799))
        ->reduce((a, v) => a .. v)
        ->setline(1)
    nno <expr> n Func()
    def g:Func(): string
        searchcount({maxcount: 1000, timeout: 500})
        return 'n'
    enddef

---

You can't just refactor  `search#index()` so that it bails out  when you're on a
long line.  *Any* long line (even before or after) can make Vim lag.

---

<https://github.com/vim/vim/pull/4446#issuecomment-702825238>

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

## cannot use dictionary function as a method

    $ vim -Nu NONE -S <(cat <<'EOF'
        let Funcref = function('strlen')
        echo 'string'->g:Funcref()
    EOF
    )

    6
    ✔

    $ vim -Nu NONE -S <(cat <<'EOF'
        let Funcref = #{key: function('strlen')}
        echo 'string'->g:Funcref.key()
    EOF
    )

    E107: Missing parentheses: g:Funcref.key()˜

Bug?  Feature request?

Update: It might be working as intended:
<https://github.com/vim/vim/issues/4768#issuecomment-518006514>

## channel-demo

According to `:h channel-demo`:

   > Instead of giving a callback with every send call, it can also be specified
   > when opening the channel: >
   >         call ch_close(channel)
   >         let channel = ch_open('localhost:8765', {'callback': "MyHandler"})
   >         call ch_sendexpr(channel, 'hello!')

It doesn't work with the python demo server.

---

I've found a way to "fix" it.
First, import it in `/tmp/demo.py`:

    :sp /tmp/demo.py
    :r $VIMRUNTIME/tools/demoserver.py

Then apply this patch (`$ cd /tmp; patch </tmp/patch.txt`):
```diff
diff --git a/usr/local/share/vim/vim82/tools/demoserver.py b/tmp/demo.py
index a9eed5e..00fe8bf 100755
--- a/usr/local/share/vim/vim82/tools/demoserver.py
+++ b/tmp/demo.py
@@ -64,7 +64,7 @@ class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
                     response = "got it"
                 else:
                     response = "what?"
-                encoded = json.dumps([decoded[0], response])
+                encoded = json.dumps([0, response])
                 print("sending {0}".format(encoded))
                 self.request.sendall(encoded.encode('utf-8'))
         thesocket = None
```
To test the fix, start the updated demo server:

    $ /tmp/demo.py

Now source this from the current Vim instance:

    mess clear

    fu! MyHandler(channel, msg)
        echom 'from the handler: ' .. a:msg
    endfu
    let channel = ch_open('localhost:8765', #{callback: 'MyHandler'})
    call ch_sendexpr(channel, 'hello!')

You should see this message in `:mess`:

    from the handler: got it

Which means the callback was correctly invoked.

What was wrong in the original demo server?

Apparently, `json.dumps()` converts this:

    ✔
    [0,"got it"]

into this:

    ✘
    [1, "got it"]

I think the  issue comes from the  first number which has  been incremented (not
from the extra space).

   > If your server sends  back multiple responses you need to  send them with ID
   > zero, they will be passed to the channel callback.

   ...

   > When the process wants to send a message to Vim without first receiving a
   > message, it must use the number zero:
   >     [0,{response}]

---

And if you want to terminate the server, just run:

    call ch_close(channel)

Then type `quit` or press `C-c` while in the demo server.

As a last resort, run:

    $ kill $(pidof python)

But bear  in mind that you  won't be able to  restart the server for  one or two
minutes:

    socket.error: [Errno 98] Address already in use

---

According to Bram:

   > Read :help channel-use, it will explain about using ch_sendexpr().
   > The callback is for NL or raw messages, you are using JSON here.

But the demo server encodes its reply in json.

Make tests to better understand *when* we can use a callback.
Here are the parameters to consider:

   - the channel can be in raw, nl, json or js mode
   - the callback can be passed to `ch_sendexpr()`, specified when opening the channel, or both
   - the server can send its reply without encoding, or it can encode it with nl, json or js

Where  is it  documented that  a  channel callback  can only  handle a  response
received after calling `ch_sendexpr()` if it's *not* encoded in json (raw or nl)?

##
## The descriptions of the local plugins are not aligned in the main help file:

    vim -Nu NORC -S <(cat <<'EOF'
        set rtp-=~/.vim
        set rtp-=~/.vim/after
        set rtp^=~/.vim/pack/mine/opt/abolish
        set rtp^=~/.vim/pack/mine/opt/asyncmake
        set rtp^=~/.vim
        set rtp+=~/.vim/after
    EOF
    )

    :h
    :norm! G

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

<https://github.com/vim/vim/pull/2409>

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

## abbreviation sometimes unexpectedly expanded inside a word

**Describe the bug**

An abbreviation is sometimes unexpectedly expanded in the middle of a word.

**To Reproduce**

Run this shell command:

    $ vim -Nu NONE -S <(cat <<'EOF'
        set bs=start
        inorea ab cd
        put! ='yyyy'
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
        au InsertEnter * let s:start_insertion = #{lnum: line('.'), col: col('.')}
        au InsertCharPre * call s:Restrict_abbreviations()
    augroup END
    def s:Restrict_abbreviations()
        var curlnum = line('.')
        if v:char =~ '\k'
            || s:start_insertion.col - 1 <= searchpos('[^[:keyword:]]', 'bn', curlnum)[1]
            || curlnum != s:start_insertion.lnum
            || state() =~ 'm'
            return
        endif
        feedkeys("\<c-v>" .. v:char)
        v:char = ''
    enddef

So far, it seems to work.

