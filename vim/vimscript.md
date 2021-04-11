# Filename expansion
## In a command which expects a filename as argument, how to represent
### any single character?

Use the wildcard `?`:

                v
    :sp /etc/env?ronment
    " edit /etc/environment

### any sequence of characters excluding a slash?

Use the wildcard `*`:

                v
    :sp /etc/env*
    " edit /etc/environment

Warning: If your command expects only one filename (like `:e` or `:sp`), and the
expansion generates more than one filename, an error may be raised:

    :sp /etc/bash*
    E77: Too many file names~

### any sequence of characters including a slash?

Use the wildcard `**`:

                               vv
    :sp | argl | args /etc/apt/**
    " all files and directories under `/etc/apt` are included in the local arglist

Here, without  the second star,  only the files and  directories at the  root of
`/etc/apt` would be included in the arglist.

### the character 'a' or 'b' or 'c'?

Use `[abc]`:

    :sp | argl | args /etc/[abc]*
                           ^----^

Here,  only the  files and  directories  starting with  `a`  or `b`  or `c`  are
included in the arglist.

##
## When should I use `glob()` instead of `expand()`?

When you're interested in *existing* filenames:

   > A name for a non-existing file is not included.

### What happens if I use it in other circumstances?

It may not generate what you expect:

    sil cd /tmp | echo glob('%:t')

Here, you  get an  empty string,  while you  probably expected  the name  of the
current file.  That's because `%:t` refers to  the name of the current file, but
there is probably no file with this name in the current working directory (which
here is `/tmp`).

---

OTOH, this would work:

    sil cd /tmp | echo glob('%:p')
                               ^

Because `%:p` refers  to the *absolute* path  to the current file,  which is not
sensitive to the current working directory.

---

Similarly, this will probably fail to expand the word under the cursor:

    echo glob('<cword>')

Unless, you have a file with the same  name as the word under the cursor in your
current working directory.

#### What should I use instead then?

`expand()` is not restricted by this limitation:

    sil cd /tmp | echo expand('%:t')

    echo expand('<cword>')

##
# Function calls
## I have many nested function calls.

    slice(strpart(getline('.'), col('.') - 1), 0, 1)

### How to make them more readable?

Unnest the calls using the method call `->` token:

    getline('.')->strpart(col('.') - 1)->slice(0, 1)
                ^^                     ^^

#### For which type of functions does this work?

Any: builtin functions, custom functions, lambdas, ...

Example:
```vim
echo 3->pow(2)
```
    9.0
```vim
vim9script
def Pow(x: number, y: number): number
    return repeat([x], y)->reduce((a, v) => a * v)
enddef
 #    custom
 #    v------v
echo 3->Pow(2)
```
    9
```vim
vim9script
 #         lambda
 #    v--------------v
echo 3->((x) => x * x)()
```
    9

Note that when  a non-builtin function is  used as a method, the  base is always
passed as the first argument.  That is,  the expression to the left of the arrow
("the base"), is passed  to the function on the right of the  arrow as its first
argument.

####
#### When can I pass such an expression to the `:call` command?

Only when it starts with a function name.

    ✔
    :call FuncA()->FuncB()

    ✘
    :call 'some string'->Func('.')
    E129: Function name required~

That's because `:call` expects a function name (it doesn't matter whether it's a
builtin or a custom one), and nothing else.

---

Note that `:call` must be followed by a function name *immediately*:

          ✘
          v
    :call !FuncA()->FuncB()
    E129: Function name required~

##### What to do when I can't?

Use `:eval`:

    :eval 'some string'->append('.')
     ^--^
      ✔

####
#### If I write `!` at the start of the expression, what is it applied to?

It's applied to the whole chain:

    !Funca()->Funcb()

    ⇔

    !(Funca()->Funcb())
     ^                ^

##### But I just want to inverse the value of the *first* function!

Use explicit parentheses to limit the scope of the `!` operator:

    (!Funca())->Funcb()
    ^        ^

##
## I have a function call with many arguments
### How can I name them to make the code more readable?

Wrap them inside a dictionary:

    def Func(arg_opts: dict<any>)
        var opts = arg_opts
    enddef
    Func({foo: 1, bar: 2, baz: 3})
               ^       ^       ^

Here, the  values `1`, `2`  and `3`  are mapped to  the names `foo`,  `bar`, and
`baz`, which can help to make them more readable.

---

Note that you could also break the arguments on multiple lines:

    Func(
        foo,
        bar,
        baz,
        ...
        )

This  kind of  formatting is  probably  portable across  many other  programming
languages (C, python, ...).

#### How to adapt this technique to set default values to arguments which might be omitted in a function call?

Use `extend()` and the optional third argument `keep`.
```vim
vim9script
def Func(arg_opts: dict<any>)
    #                             default values
    #                           v----------------v
    var opts = extend(arg_opts, {a: 1, b: 2, c: 3}, 'keep')
    #          ^-----^                              ^----^
    echo opts
enddef
Func({b: 4})
```
    {'a': 1, 'b': 4, 'c': 3}

Notice how in  the function's body, the dictionary `opts`  includes the keys `a`
and `c` with the  values `1` and `3`, even though we didn't  specify them in the
function call.  This shows that, in effect, any argument is optional.

Technically, we extend the dictionary argument with options from another one.
The latter contains our default options, in case the former lacks some of them.
The third argument `keep` is necessary to give the priority to a supplied option
in case it conflicts with a default one.

Note that this is an ad-hoc mechanism.
In the future, Vim may provide a builtin one; see `:h todo /named arguments`:

   > Implement named arguments for functions with optional arguments:
   >     func Foo(start, count = 1, all = 1)
   >     call Foo(12, all = 0)

###
### how to reduce their number (knowing that some of them can be derived from a single expression)?

Pass the expression from which some of the arguments can be derived, and let the
function compute the arguments inside its body.

Example:
```vim
vim9script
def Foo()
    var view = winsaveview()
    var lnum = view.lnum
    var col = view.col
    Bar(lnum, col)
    #   ^-------^
    #   2 arguments
enddef
def Bar(...l: any)
enddef
```
    →
```vim
vim9script
def Foo()
    var view = winsaveview()
    Bar(view)
    #   ^--^
    #   1 argument
enddef
def Bar(v: dict<number>)
enddef
```
##
## How to avoid
### repeating the same argument(s) in several calls to the same function?

Use a partial:
```vim
vim9script
def Func(a: number, b: number, c: any = v:none, d = 0)
    if typename(c) == 'number'
        echom printf('received 4 arguments: %d, %d, %d, %d', a, b, c, d)
    else
        echom printf('received 2 arguments: %d, %d', a, b)
    endif
enddef
var Partial = function(Func, [1, 2])
Partial()
Partial(3, 4)
```
    received 2 arguments: 1, 2
    received 4 arguments: 1, 2, 3, 4

---

Without a partial, you would have to write:

    Func(1, 2)
    Func(1, 2, 3, 4)

---

Analogy: Just like you can tattoo some  drawing(s) on a person, you can "tattoo"
arguments on a function; it then becomes a partial.

### repeating the same arguments in several calls to different functions?

Assign them to a list, and pass the latter to the function with `call()`:
```vim
vim9script
def Add(...l: list<number>)
    echo l->reduce((a, v) => a + v)
enddef
def Multiply(...l: list<number>)
    echo l->reduce((a, v) => a * v)
enddef
var args = [1, 2, 3]
call(Add, args)
call(Multiply, args)
```
    6
    6

Without `call()`, you would had to write:

    Add(1, 2, 3)
    Multiply(1, 2, 3)

---

Btw, `call()` is useful even if there are non-repeating arguments before/after:
```vim
vim9script
def Add(...l: list<number>)
    echo l->reduce((a, v) => a + v)
enddef
def Multiply(...l: list<number>)
    echo l->reduce((a, v) => a * v)
enddef
var args = [1, 2, 3]
call(Add, args + [4, 5])
call(Multiply, [6, 7] + args)
```
    15
    252

---

Analogy: Just like you can put several gifts  inside a packaging to send them to
a person, you  can "package" arguments in a  list and pass it to  a function via
`call()`.

##
## Optional arguments
### I've specified a default expression to a function argument to make it optional at the call site:

In the function header, assign it the default expression after an equal sign:
```vim
vim9script
def Order(food: string, howmany = 10)
    echo printf('I need %d %s', howmany, food)
enddef
Order('carrots', 3)
Order('onions')
```
    I need 3 carrots
    I need 10 onions

#### The default expression is evaluated
##### at the time of:  the function definition, or the function call?

At the  time of the  function call.   This lets you  use an expression  which is
invalid the moment the function is defined.
```vim
vim9script
 #                                not defined yet
 #                                v
def Order(food: string, howmany = n)
    echo printf('I need %d %s', howmany, food)
enddef
var n = 10
Order('carrots', 3)
Order('onions')
```
    I need 3 carrots
    I need 10 onions

Here, notice  how no error  is raised,  even though `n`  did not exist  when the
function was defined.

##### all the time, or only when no matching argument was specified during a call?

Only when no matching argument was specified during a call.
```vim
vim9script
var list = [1, 2, 3]
def Func(l = map(list, (_, v) => v + 1))
enddef
Func([])
echo list
```
    [1, 2, 3]
```vim
vim9script
var list = [1, 2, 3]
def Func(l = map(list, (_, v) => v + 1))
enddef
Func()
echo list
```
    [2, 3, 4]

Notice how  in the  first example,  `list` is  not altered,  because a  list was
passed to `Func()` when the latter was called, thus Vim did not have to evaluate
the default expression to get a value.

OTOH, in the second  example, `list` *is* altered because no  list was passed to
`Func()`, thus Vim had to evaluate the default expression to get a value.

####
#### On which condition can I refer to an argument in a default expression?

The argument you want  to refer to must be positioned  *before* the one matching
your default expression.

So, this works:
```vim
vim9script
def Order(food: string, howmany = food == 'carrots' ? 3 : 5)
    echo printf('I need %d %s', howmany, food)
enddef
Order('carrots')
```
    I need 3 carrots
           ^
```vim
vim9script
def Order(food: string, howmany = food == 'carrot' ? 3 : 5)
    echo printf('I need %d %s', howmany, food)
enddef
Order('tomatoes')
```
    I need 5 tomatoes
           ^

But not this:
```vim
vim9script
def Order(food = howmany == 3 ? 'carrots' : 'tomatoes', howmany = 3)
    echo printf('I need %d %s', howmany, food)
enddef
Order()
```
    E121: Undefined variable: howmany

####
### My function accepts 2 optional named arguments.
```vim
vim9script
def Order(food: string, howmany = 10, when = 'tomorrow')
    echo printf('I need %d %s before %s', howmany, food, when)
enddef
```
#### How to specify a value for the 2nd argument, without re-specifying the default expression of the 1st one?

Use the special value `v:none`.
```vim
fu Order(food, howmany = 10, when = 'tomorrow')
    echo printf('I need %d %s before %s', a:howmany, a:food, a:when)
endfu
call Order('carrots', v:none, 'tomorrow')
 "                    ^----^
```
    I need 10 carrots before tomorrow
           ^^
---

Note that  this means  you cannot  pass `v:none`  as an  ordinary value  when an
argument  has a  default expression.   Being able  to use  named arguments  in a
function call could work around this issue.  See `:h todo /named arguments`:

   > Implement named arguments for functions with optional arguments:
   >     func Foo(start, count = 1, all = 1)
   >     call Foo(12, all = 0)

##
# Heredoc
## Can I start a line with a backslash inside a heredoc?

Not for the first one:

    " ✘
    let lines =<< trim END
        \a
        b
        c
    END
    E990: Missing end marker 'ENDa'~

That's because the line continuation is used before the command is parsed.

If your first item needs to start with a backslash, do this:

    let cpo_save = &cpo | set cpo+=C
        let lines =<< trim END
        \a
        b
        c
    END
    let &cpo = cpo_save
    echo lines
    ['\a', 'b', 'c']~

Or this:

    let lines =<< trim END
        b
        c
    END
    let lines = ['\a'] + lines
    echo lines
    ['\a', 'b', 'c']~

The other lines can start with a backslash:

    " ✔
    let lines =<< trim END
        a
        \b
        \c
    END
    echo lines
    ['a', '\b', '\c']~

## If I use the `trim` argument, how much leading whitespace does Vim trim?

Vim trims any leading whitespace matching the indentation of the first non-empty
(`!~ '^$'`) text line inside the heredoc:

    let list =<< trim END
      xx
    xx
        xx
    END
    echo list
    ['xx', 'xx', '  xx']~
                  ^^
                  there were 4 spaces initially,
                  but 2 were trimmed because there were 2 on the first text line

Note that Vim makes a distinction between tabs and spaces.

---

Exception: on the last line containing the  marker, Vim trims only a sequence of
leading whitespace if it matches *exactly* the one on the line containing `=<<`.
IOW, there must not be less *or more* whitespace.
This explains why the assignment fails when there are *fewer* spaces on the last
line than on the first line:

        let list =<< trim END
    2 spaces below
    vv
      END
        echo list
        E990: Missing end marker 'END'~

##
# Pasting text
## What are the pros of using `:pu=` over `append()` or `setline()`?

`:pu=` is more handy on the  command-line, in an interactive usage, because less
verbose.

Also, it moves the cursor on the last line pasted.
This is handy when you have multiple blocks of text to paste.

With `append()` and `setline()`, you would have to re-compute the line address
from which you want to paste every block, to avoid that they overlap.

## What are the cons of using `:pu=`?

   - the cursor moves
   (which may be undesirable when you only have one paste to do)

   - it's not silent
   (you have to prefix it with `:silent`)

   - you have to escape double quotes

   - it doesn't delete the initial empty line in a new buffer

   - it pollutes the expression register

## When should I use `append()`?

When you need to INSERT a single block of text in an EXISTING buffer.

## When should I use `setline()`?

When you need to REPLACE a set of lines in an existing buffer.
Or, when you need to ADD new lines in:

   - a new buffer
   - at the end of an existing buffer, whose last line is empty

###
## What can `setline()` do that `append()` can't?

`setline()` can delete the contents of an existing line.
`append()` will NEVER delete any existing contents.

## Can `setline()` add new lines?

Yes, but only if there're no more lines to replace.
In this  case, `setline()` WILL  add just  enough so that  it can paste  all the
lines it received as argument.

###
## What happens if I call `setline(0, ...)`?

There's no line 0, and `setline()` can only replace FROM an existing line.
So, it won't paste anything.

## What happens if I call `append(0, ['foo', 'bar'])` in a new buffer?

You get an empty line, 'foo', then 'bar'.

Where does the empty line come from?
Think like this:

   > “append() INSERTS lines between 2 existing lines”

When  you pass  it the  address  `0`, it  inserts  'foo' and  'bar' between  the
UNexisting line 0 and the existing line 1.
IOW, ABOVE line 1.
The empty line is the old line 1.

## What happens if I execute `:pu=['foo', 'bar']` in a new buffer?  What's the difference with the previous `append()`?

Like with the previous `append()`, you get an empty line, 'foo', then 'bar'.
Unlike the previous `append()`, the cursor moves on the 'bar' line.

###
## How to use `append()` and make the cursor move like `:pu=`?

    :let lines = [...]
    :call append('.', lines) | exe '+'.len(lines)

## What happens if I use `setline()` to replace 10 lines while there're only 5 below?

It will create 5 new lines, so that  it can replace their empty contents.

##
# Searching text
## My cursor is on the third line in this file:

    x


    x

### What will be the output `:echo search('x', 'n', 2)`?

`0`

### What does it imply regarding the stopline argument?  (2)

You may  have thought  that the stopline  would have no  effect, because  it was
before the current  line, and that the  output would be `4`; but  that's not the
case.

The stopline argument is processed independently  from the current line; it does
not mean:

    "search from the current line up/down to the stopline"
            ^-------------------^

but:

    "ignore every line after/before the stopline"

---

This also implies that the flag `W` is useless with a stopline.
Suppose you  don't use the  flag `b`; the  stopline will make  `search()` ignore
every line after.
As a result, `search()` can *not* reach the end of the file, and `W` is useless.
Something similar  happens if you use  `b`; `search()` can't reach  the start of
the file.

##
## Inside a `while` loop, which flag should I
### always pass to `search()`?

`W`

Otherwise, the loop will probably never ends.

### never pass to `search()`?

`c`

Same reason as previously.

##
# How to get the number of matches of an arbitrary pattern in the current buffer?

    :echo searchcount({'pattern': 'pat'}).total

## What happens if I don't provide a pattern?

The search register is used.

#
## How to be sure that *all* matches are found?

Set `maxcount` to 0  to lift the upper limit on the number  of matches which can
be  found.   And  set  `timeout`  to  0 to  disable  the  time  out  during  the
recomputing.

    :echo searchcount(#{pattern: '.'})
    {'exact_match': 0, 'current': 100, 'incomplete': 2, 'maxcount': 99, 'total': 100}~
                                                                                 ^-^

                                                v           v
    :echo searchcount(#{pattern: '.', maxcount: 0, timeout: 0})
    {'exact_match': 1, 'current': 1000, 'incomplete': 0, 'maxcount': 0, 'total': 4913}~
                                                                                 ^--^

## What happens to `total` if there are more matches than `maxcount`?

It's set to `maxcount + 1`.

    :echo searchcount(#{pattern: '.'})
    {'exact_match': 0, 'current': 100, 'incomplete': 2, 'maxcount': 99, 'total': 100}~
                                                                                 ^-^
                                                                                 99 + 1

###
## How to get the index of the match under the cursor?

Inspect the `current` key:

    :echo searchcount(#{pattern: 'pat'}).current
                                        ^------^

### What does this output if I'm not on a match?

The index of the previous match; and if there's no previous match, 0.

## How to get the index of the match at an arbitrary position?

Pass a dictionary  to `searchcount()` which includes the `pos`  key, and a value
describing the position you're interested in:

    $ vim -Nu NONE +"let @/ = 'pat' | sil pu!=['xxx', 'pat']->repeat(3)"
                        v---------v
    :echo searchcount(#{pos: [4,1,0]}).current
    2~

Here, `searchcount()` tells you that the index of the match on line 4 column 1 is 2.
If you had not passed the dictionary, `searchcount()` would have returned 3, because
that's the index of the match on the last line of the buffer where the cursor is.

---

`pos` has an effect on `current` *and* `exact_match`.

##
## How to check whether
### the cursor is on a match?

Inspect the `exact_match` key (its value is a boolean):

    if searchcount(#{pattern: 'pat'}).exact_match
        " the cursor is on a match
    endif

### the results are unreliable because
#### finding all the matches took too much time?

Inspect the `incomplete` key; it should be 1 in that case.

#### there were more matches than `maxcount`?

Inspect the `incomplete` key; it should be 2 in that case.

##
## What's the effect of `recompute: 0`?

It makes `searchcount()`  give the results relevant for the  last `/`, `?`, `n`,
`N` command,  or for the  last invocation  of the function;  but only if  `S` is
absent from `'shm'`.

    $ vim -Nu NONE +"set shm-=S | let @/ = '.' | pu!='xxxxx'"
    " press:  n $
    :echo searchcount(#{recompute: 0})
    {'exact_match': 1, 'current': 2, 'incomplete': 0, 'maxcount': 99, 'total': 5}~
                                  ^
    :echo searchcount()
    {'exact_match': 1, 'current': 5, 'incomplete': 0, 'maxcount': 99, 'total': 5}~
                                  ^

If `S` is in `'shm'`, then it  gives the results relevant for the current cursor
position.  This  is because, in that  case, there is no  previous computed value
which `searchcount()` could return; it has to (re)compute.

Whether `S` is in `'shm'` or not, a possible `pattern` key is ignored.
That is, `searchcount()`  uses either `@/` or the last  pattern `key`, depending
on what was the last command (`/`, `?`, `n`, `N` vs `:call searchcount()`).

##
# Antipatterns
## When can I simplify `filter(...)->empty()`?

When the condition passed to `filter()` is a simple regex or string comparison.

### How to simplify it?

Use `index(...) == -1` or `match(...) == -1`.

If the test is inverted by a bang, then replace `== -1` with `>= 0`.

---

For example, to express that a list contains an item matching a pattern, write this:

    match(list, pat) >= 0

and not this:

    !copy(list)->filter((_, v) => v =~ pat)->empty()

---

As another example, to express that there's no location window anywhere, write this:

    getwininfo()->map((_, v) => v.loclist)->index(1) == -1

and not this:

    !getwininfo()->map((_, v) => v.loclist)->filter((_, v) => v)->empty()

You could even write:

    getwininfo()->match("'loclist': 1") == -1

This works  because each item in  the output of `getwininfo()`  is a dictionary,
and in that case `match()` uses a dictionary as a string.

Although, it feels awkward and brittle...
What  if one  day the  output of  `getwininfo()` uses  double quote  to surround
`loclist`, or adds/removes a space after `:`?
You would need a more permissive pattern.

#### Why should I do it?

It's shorter, and thus a little more readable.

There's  less risk  of an  unexpected side effect;  indeed, `filter()`  operates
in-place, which often requires you not to forget to use `copy()` or `deepcopy()`.

#### When is such a simplification impossible?

When the condition passed  to `filter()` is more complex than  a simple regex or
string comparison:

    copy(list)->filter((_, v) => v.foo == 1 && v.bar != 2)->empty()
                                 ^----------------------^
                                 assume that `list` contains dictionaries with the keys `foo` and `bar`

##
## ?

In  the past,  we might  have  used `glob()`  + `filter()/match()`  to test  the
presence of a file in a directory; or to find some file(s) in a directory.
That's inefficient.  Use `readdir()` instead.

    \C\<glob(

A `glob()` whose first  argument is a file pattern containing  a wildcard in the
last path component is a good candidate for a refactoring.

Example:

    glob('~/.config/keyboard/*', false, true)

    →

    readdir($HOME .. '/.config/keyboard/')
        ->map((_, v) => $HOME .. '/.config/keyboard/' .. v)

Although, note  that `readdir()` might make  the code more verbose  (if you need
absolute file  paths).  In that  case, you can  keep `glob()`, provided  that it
doesn't have a  too bad impact on performance (i.e.  not invoked too frequently,
and expands a directory with not too many files).

Other example:

    # test that a file containing "some_name" is in the directory of the current file
    if !glob(expand('%:p:h') .. '/*', false, true)
        ->filter((_, v) => v =~ 'some_name')
        ->empty()

        # do sth
    endif

    if !expand('%:p:h')
        ->readdir((n: string): bool => n =~ 'some_name')
        ->empty()

        # do sth
    endif

It is *much* faster.

### ?

Usage example for `readdir()`:

    vim9 echo readdir('/etc', (n: string): bool => n =~ 'network', {sort: 'none'})
    ['network', 'networks']~

---

If you  need to filter out  entries based on  something else than the  name, use
`readdirex()`:

    vim9 echo readdirex('/etc', (e: dict<any>): bool => e.name =~ 'network' && e.user == 'root', {sort: 'none'})
    [{~
      'group': 'root',~
      'perm': 'rwxr-xr-x',~
      'name': 'network',~
      'user': 'root',~
      'type': 'dir',~
      'time': 1468960975,~
      'size': 0},~
    {~
      'group': 'root',~
      'perm': 'rw-r--r--',~
      'name': 'networks',~
      'user': 'root',~
      'type': 'file',~
      'time': 1445534121,~
      'size': 91,~
    }]~

### ?

There is an extra benefit for using `readdir()` instead of `glob()`.
It gives you the hidden entries too.

With `glob()`, you would need 2 invocations:

      glob(dir .. '/.*', false, true)
    + glob(dir .. '/*', false, true)

But even then, you would still need to remove 2 garbage entries:
```vim
vim9script
mkdir('/tmp/dir', 'p')
writefile([], '/tmp/dir/.hidden')
echo glob('/tmp/dir/.*')
```
    /tmp/dir/.
    /tmp/dir/..
    /tmp/dir/.hidden

To document.

### ?

`readdir()` ignores `'wildignore'` (and `'suffixes'`).
`glob()` does not; unless you pass it a second `true` argument.

### ?

`glob()` is much slower when it has to honor `'wildignore'` (and `'suffixes'`).
If you  have to use `glob()`,  pass it `true`  as a second argument,  unless you
really need to honor those options.  Same remark for `globpath()` (probably).

##
## The next expression uses a ternary conditional:

    name == 'foo'
    ?     1
    : name == 'bar'
    ?     2
    :     3

### How should I rewrite it?

    {foo: 1, bar: 2, baz: 3}[name]

Or:

    get({foo: 1, bar: 2}, name, 3)

---

Use the first expression if you know the third value which can be assigned to `name`.
Use the second one if you don't know what other value(s) can be assigned to `name`.

#### Why?

  - more concise/readable

  - mentions explicitly the third value `baz` in the first case
    (before it was implicit/not mentioned at all)

  - easier to expand later if `var` can have more values

##
# Miscellaneous
## How to save/restore the cursor position?

Use `getcurpos()` and `setpos()`:

    let pos = getcurpos()
    ...
    call setpos('.', pos)

Do *not* use `getpos()`; it does not preserve the `curswant` number.

`getpos()` is fine though if:

   - you need to save the position of a mark
   - you don't care about `curswant`, and you just need the line/column number

---

The help at `:h setpos()` seems contradictory.

On the one hand, it says:

   > The "curswant" number is only used when setting the cursor
   > position.  It sets the preferred column for when moving the
   > cursor vertically.

then later, it says:

   > This does not restore the preferred column for moving
   > vertically; if you set the cursor position with this, |j| and
   > |k| motions will jump to previous columns!  Use |cursor()| to
   > also set the preferred column.

I think the second paragraph is older.
When it was written, `setpos()` could not  set `curswant`; but now it can, hence
the first paragraph, which was added later.

Anyway, in my limited testing, `setpos()` *can* correctly set `curswant`.
For example, try this minimal vimrc:

    pu! =range(97, 122)->map((_, v) => nr2char(v))->join('')
    t.
    call setpos('.', [bufnr(), line('.'), col('.'), 0, 12])
    norm! k

Notice that the  `k` motion has made  the cursor move onto the  character `l` of
the first  line of  text, instead  of `a`;  this is  because `setpos()`  has set
`curswant` to the value 12, and `l` is the 12th character on the line.

## How to break the undo sequence without entering insert mode?

    let &ul = &ul

Test:

    $ vim -Nu NONE +"call setline(1, ['a', 'b'])"

    :1d | 1d
    :undo
    a~
    b~

    $ vim -Nu NONE +"call setline(1, ['a', 'b'])"
    :1d | let &ul = &ul | 1d
    :undo
    b~
    :undo
    a~
    b~

Source: <https://vi.stackexchange.com/a/26475/17449>

##
## Vim has been started by another process.  How can I get the full pathname of its command?

    :echo $_

From `man bash /^\s*_`:

   > _      ...
   >        Also set  to the full pathname  used to invoke each  command executed
   >        and placed in the environment exported to that command.

From `man zshparam /^\s*_`:

   > _ <S> ...
   >       Also,  this parameter  is  set  in the  environment  of every  command
   >       executed to the full pathname of the command.

Usage example:

    $ ls | vipe
    :echo $_
    /usr/bin/vipe~

    $ cd ~/Vcs/vim
    $ git commit --amend
    :echo $_
    /usr/bin/git~

##
## How to get the path to the parent of
### a given file?

Use `fnamemodify()` and `:p:h`:

    echo fnamemodify($MYVIMRC, ':p:h')
    /home/user/.vim~

### a non-existing directory?

Use `fnamemodify()` and `:p:h`:

    echo fnamemodify($HOME .. '/.vam', ':p:h')
    /home/user~

### an existing directory?

Use `fnamemodify()` and `:p:h:h`:

    echo fnamemodify($HOME .. '/.vim', ':p:h:h')
    /home/user~

---

You  need two  `:h`  because `:p`  adds  a trailing  slash to  the  path if  the
directory exists.

    echo fnamemodify($HOME .. '/.vim', ':p')
    /home/user/.vim/~
                   ^
    echo fnamemodify($HOME .. '/.vam', ':p')
    /home/user/.vam~
                   ^

This has an effect on the `:h` modifier, because the latter considers a trailing
slash as a (empty) path component.

##
## How to get the width of the number column?  (whether it's visible doesn't matter)

    :echo max([line('$')->len(), &l:numberwidth - 1])

## How to get the width of all the *currently visible* fold/number/sign columns?

    :echo wincol() - virtcol('.')

This assumes that  the text before the  cursor is shorter than the  width of the
window.  It doesn't  matter whether the line  is wrapped or not;  in both cases,
`virtcol('.')` will be too big.

If you need a workaround, try to evaluate the expression from the first column:

    :norm! 0
    :echo wincol() - virtcol('.')

If you're inside an `<expr>` mapping, you can't execute `:norm!`; it would raise `E523`:

    E523: Not allowed here

Use `cursor()` instead:

    cursor(0, 1)

##
## How to get the name of the current script, from the script itself?

    expand('<sfile>')

Note that this must be evaluated at the script level, not from a function.

## How to get the stack of function calls which lead to the calling of the current function?

    expand('<stack>')

Usually, the stack is displayed with the following template:

    function FuncA[123]..function FuncB[456]..function CurrentFunction

If a script is sourced at the start, it is printed in the stack:

    /path/to/some/scrippt[123]..function FuncA[456]..function FuncB[789]..function CurrentFunction
    ^------------------------^

If a script is sourced at any other point, it is printed in the stack, *and* its
name is preceded by `script `:

    function FuncA[123]..function FuncB[456]..script /path/to/some/scrippt[789]..function CurrentFunction
                                              ^-----^

### What's the difference between the last two special sequence of characters?

`<sfile>` can print the call stack only from a function.
`<stack>` can print the call stack from a function *and* at the script level.

In general, it's better to always use `<stack>` to get the call stack; it's more
readable and more reliable.

##
## How to play a sound?

Use `sound_playfile()` or `sound_playevent()`.

For example, you could download the intro music for the PlayStation 1:

    $ youtube-dl -x --audio-format vorbis -o 'ps.%(ext)s' 'https://www.youtube.com/watch?v=oAhvQoLpvsM'

Then, play it when Vim starts, adding this code to your vimrc:

    augroup play_ps_sound_on_vimenter
        au!
        au VimEnter * call sound_playfile('/tmp/ps.ogg')
    augroup END

Note that you really need `%(ext)s` in  the value passed to the argument `-o` of
`youtube-dl(1)`; I think that's because the latter expects a template.
You could  write `ps.ogg` directly, and  `mpv(1)` would play the  file (although
with a warning message, I think), but not Vim.

---

The `complete` "event" is a nice and probably useful sound:

    call sound_playevent('complete')

As an example, it could be played after an async command has finished populating the qfl.

## How to clear the undotree of a file?

Perform some edit while `'undolevel'` is set to `-1`:

    setl ul=-1
    exe 'norm! "=""' .. "\r" .. 'p'

In a script:

    let [ul_save, bufnr] = [&l:ul, bufnr('%')]
    setl ul=-1
    try
        exe 'norm! "=""' .. "\r" .. 'p'
    finally
        call setbufvar(bufnr, '&ul', ul_save)
    endtry

For more info, see `:h clear-undo`.

##
## What happens if
### I refer to the variable `foo#bar#var` while it doesn't exist?

Vim looks for an autoload file `bar` in a directory `bar`.
If one is found,  it's sourced, and if `foo#bar#var` is set  in the latter, your
variable reference won't raise any error.

    $ mkdir -p /tmp/some/autoload/foo

    $ cat <<'EOF' >/tmp/some/autoload/foo/bar.vim
        let foo#bar#var = 123
        echom 'all the script is sourced'
    EOF

    $ vim -Nu NORC --cmd 'set rtp^=/tmp/some' +'echo foo#bar#var'
    123~

The message "all the script is sourced" shows that Vim sources the entire script.
It doesn't merely look for a `foo#bar#var` assignment.

For more info, see `:h autoload`.

### I assign a value to the variable `foo#bar#var`?

Aside from the variable being assigned a value, nothing.
In particular, no autoload script is sourced.

    $ mkdir -p /tmp/some/autoload/foo

    $ cat <<'EOF' >/tmp/some/autoload/foo/bar.vim
        unsilent echom 'all the script is sourced'
    EOF

    $ vim -Nu NORC --cmd 'set rtp^=/tmp/some' +'let foo#bar#var = 123'

This time, the message "all the script is sourced" is not printed.

##
## How to implement a custom completion for `input()`?

Use its third optional argument.
Give it the value `custom,CompletionFunc`.

    vim9script
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

---

Note that you are not limited to a custom completion function.
You  can leverage  any type  of completion  which is  available in  a custom  Ex
command, like `file` for file completion (as used in `-complete=file`).

    let fname = input('File: ', '', 'file')

## How to install vim-vint?

    $ git clone https://github.com/Kuniwak/vint
    $ cd !$:t
    $ python3 -m pip install --user --upgrade .

    $ cd ..

    $ git clone https://github.com/pypa/setuptools_scm
    $ cd !$:t
    $ python3 -m pip install --user --upgrade .

##
# Pitfalls
## Do *not* use a function which has a side effect as the third argument of `get()`!

Example:

    let buf = get(s:, 'buf', term_start(&shell, #{hidden: 1}))

If this statement can be executed multiple  times during the same Vim session, a
new hidden terminal buffer will be created each time, which is probably not what
you want.

This is because the arguments passed to `get()` are evaluated *before* the latter.
IOW,  when `get()`  checks  whether `s:buf`  exists, it's  already  too late  to
prevent `term_start()` from being evaluated.

Instead, write this:

    let buf = exists('s:buf') ? s:buf : term_start(&shell, #{hidden: 1})

This time, the third operand of `?:` will be evaluated only if the first operand
is false; i.e. only if `s:buf` does not exist.

##
## When should I include a guard at the top of an autoloaded script?

Whenever the latter sets some variable or interface (mapping, autocmd, command).

### Why?

Suppose that your  script has an internal state which  is initialized by setting
some script-local variable (updated at runtime):

    let s:var = {}

If the script is  sourced a second time, the variable will be  reset, as well as
the internal  state of the  script.  In effect, this  will tell the  script that
it's in the same state as if Vim had just started.
This is a lie;  you may have been using Vim for quite  some time.
This reset state may not be adapted to the state in which Vim is currently.
It may break assumptions on which you rely in other parts of the script.

#### But how an autoloaded script could be sourced twice?

Suppose you need to call a function defined in your script from somewhere else:

    call script#func()

You write the  name of the function  correctly, except you make a  small typo in
the last component (i.e. the text after the last `#`):

    call script#funx()
                   ^
                   ✘

When this function call is processed, suppose that the script has *already* been
sourced because another function from it  was called earlier.  Vim sees see this
wrongly spelled function is not defined; so,  it has to look for its definition.
The path  *before* the last  component being correct,  it finds the  script, and
sources it *again*.  Because of the typo,  it doesn't find the function, but the
damage is done: the script has been sourced twice.

See also:
<https://vi.stackexchange.com/questions/22374/why-are-inclusion-guards-used-in-vim-plugins>

##
## When should I use
### `==`, `==#`, `is#`?

Here's what I recommend:

   - use `is#` if one of the operand is a string

   - use `==#` if one of the operand is a list/dictionary

   - use `==` otherwise

---

Note that you can't use `is#` if the operands are lists/dictionaries:

    :echo ['a'] is# ['a']
    0~

    :echo {'k': 'v'} is# {'k': 'v'}
    0~

But you *can* if one of the operands is the *member* of a list/dictionary:

    :echo ['a'][0] is# 'a'
    1~

    :echo ['a'][0] is# ['a'][0]
    1~

    :echo {'k': 'v'}.k is# 'v'
    1~

    :echo {'k': 'v'}.k is# {'k': 'v'}.k
    1~

---

For  a list,  `==#` is  only useful  if  it contains  at least  one string  with
alphabetical characters; but let's make things  simple: one operator per type of
data.

### the function-local scope `l:`, explicitly?  (2)

When your variable stores a funcref without any scope.

If you don't, there is a risk of conflict with a public function.

---

When your variable name is one of:

   - count
   - errmsg
   - shell_error
   - this_session
   - version

In that case, without an explicit scope, Vim assumes `v:`.

Source: <https://github.com/Kuniwak/vint/issues/245#issuecomment-337296606>

It seems to be true, if you look at the source code:
<https://github.com/vim/vim/blob/a050b9471c66b383ed674bfd57ac78016199d972/src/evalvars.c#L38-L61>

If you search for `VV_COMPAT`, you only find these 5 variables atm.

If you're concerned by  a conflict with a `v:` variable, write  this line at the
top of your script:

    :scriptversion 3
                   ^
                   or any number bigger than 3

##
## Why should I prefix any call to `system[list]()` with `:silent`?

When vim is running, the terminal is in “raw” mode: it sends a character as soon
as it receives one.

But when  you execute  a shell  command (via `:!`  or `system()`),  the terminal
switches to “cooked” mode: it buffers the received characters until a CR.

This allows the terminal to implement some rudimentary line-editing functions.
But when the  terminal is in cooked  mode, some stray characters may  be left on
the screen, forcing you to `:redraw`.

MWE:

    :call system('sleep 3')
    " smash the 'l' key
    " ✘ `l` is printed on the command-line~

    :sil call system('sleep 3')
    " smash the 'l' key
    " ✔ nothing is printed on the command-line~

## When can I *not* add a comma after the last item of a list?

When the list is the left operand of an assignment (`:h :let-unpack`):

    let [a,b,c,] = [1,2,3]
    "         ^
    "         ✘
    E475: Invalid argument: ] = [1,2,3]~

##
## Sometimes, `getpos()` reports 2147483647 for the column position of the `'>` or `']` mark!
```vim
vim9script
setline(1, 'some text')
exe "norm! V\e"
echom getpos("'>")
```
    [0, 1, 2147483647, 0]

   > That's intentional. Vim defines a MAXCOL value which is used to
   > indicate the cursor is at the end of the line without specifically
   > requiring knowing the line length ahead of time. This allows the
   > behavior to stay the same even if the line length changes. Some of its
   > uses are purely internal, but it does have external visibility in the
   > case of commands like getpos().

Source: <https://groups.google.com/g/vim_dev/c/oCUQzO3y8XE/m/opuczWwCtCsJ>

Workaround:
```vim
vim9script
setline(1, 'some text')
exe "norm! V\e"
var pos: list<number> = getpos("'>")
pos[2] = col([pos[1], '$'])
echom pos
```
    [0, 1, 10, 0]

##
## Why should I avoid
### replacing `matchstr()->len()` with `matchend()`?

They are not always equivalent:

    " equivalent
    :echo matchend('### title', '^#\+')
    3~
    :echo matchstr('### title', '^#\+')->len()
    3~

    " NOT equivalent
    :echo matchend('title', '^#\+')
    -1~
    :echo matchstr('title', '^#\+')->len()
    0~

### `:k` or `:mark` to set a mark on the current position, and prefer `:norm! m` instead?

With  `:k`   and  `:mark`,  the   column  position  always  matches   the  first
non-whitespace character on the line.
Because of this,  jumping to the mark  doesn't always restore the  cursor on the
original position where you set the mark; you lose the column position.

    " execute this command while your cursor is on the `a` character
    :k a
    :echo getpos("'a")[2]
    5~
    " the original column was 8

### concatenating commands in an `:if` or `:try` block on a single line with bars

Because if  the command inside  the block  is unknown, the  rest of the  line is
ignored, which includes `| endif`; this causes an unexpected `E171` error:
```vim
if 0 | unknown | endif
```
    E171: Missing :endif

Similar issue with `:try`:
```vim
try | unknown | catch | endtry
```
    E492: Not an editor command:  unknown | catch | endtry

---

This can even change the logic of your code.
```vim
vim9script
var files = ['/tmp/do_NOT_delete_me', '/tmp/delete_me']
writefile([], files[0])
writefile([], files[1])
if 1
    if has('missing_feature') | use_missing_feature | endif
    filter(files, (_, v) => v !~ 'NOT')
endif
delete(files[0])
if 1
    finish
endif
```
Here, the  snippet has removed  the file  `do_NOT_delete_me`, and kept  the file
`delete_me`, without any error being raised.  That was *not* its purpose at all.

---

   > Consider this:
   > if has('nothing') | let x = doesnotexist | endif
   > Here you do not want to give an error for "doesnotexist".
   > Many conditions with has() depend on this.
   > Obviously, this doesn't work very well for a syntax error.
   > But it's hard to make a difference.
   > And the example for using "->" also shows that you do want to skip expressions,
   > and errors in expressions, in a version of Vim that doesn't support that.
   >
   > So, we can only document that the "endif" should be on a separate line.

See: <https://github.com/neovim/neovim/issues/12009#issuecomment-599021395>
And `:h has() /this->breaks`.

#### What should I do instead?

Make sure to break the line at least right after the unknown command:
```vim
if 0 | unknown
endif
```
    no error
```vim
try | unknown
catch | endtry
```
Alternatively, delay the parsing of `:unknown` with an `:exe`:
```vim
try | exe 'unknown' | catch | endtry
```
    no error

##
# Issues
## Why does  `:call system('grep -IRn pat * | grep -v garbage >file')`  fail to capture the standard error in `file`?

The pipe between the  two greps redirects only the standard  output of the first
grep, not its standard error.

If you really want the errors too, then group the commands:

    { grep -IRn pat * | grep -v garbage  ;} >file 2>&1
    ^                                    ^^

## Why should I avoid ``expand('`shell cmd`')`` and use `system('shell cmd')[:-2]` instead?

Sometimes it doesn't work as expected:

MWE:

    $ mkdir -p /tmp/foo; cd /tmp/foo; \
      vim -es -Nu NONE +"pu=expand(\\\"`pidof vim | awk '{print $1}'`\\\")" +'%p|qa!'
      1234~

    $ mkdir -p /tmp/foo; cd /tmp/foo; \
      vim -es -Nu NONE +'set wig+=*/foo/*' +"pu=expand(\\\"`pidof vim | awk '{print $1}'`\\\")" +'%p|qa!'
                       ^-----------------^
      ''~

To avoid this pitfall, you need to pass a non-zero value as a second argument to `expand()`:

    $ mkdir -p /tmp/foo; cd /tmp/foo; \
      vim -es -Nu NONE +'set wig+=*/foo/*' +"pu=expand(\\\"`pidof vim | awk '{print $1}'`\\\", v:true)" +'%p|qa!'
                                                                                               ^----^
      1234~

---

In any case, it's not a well-documented construct.
This has only a few relevant matches:

    :helpg \%(expand\|glob\)(['"]`

So, it's probably not well-tested.

##
# Todo
## To document
### mapnew() uses a shallow copy

See: <https://github.com/vim/vim/issues/7400#issuecomment-737411165>

This matters if:

   - you pass a list or dictionary to `mapnew()`
   - the items are themselves composite
   - you *mutate* the items

In that case, you will need `deepcopy()` + `map()`:
```vim
vim9script
var ld = [{x: 12}]
mapnew(ld, (_, v) => extend(v, {y: 34}))
echo ld
```
    [{'x': 12, 'y': 34}]
             ^-------^
                 ✘
```vim
vim9script
var ld = [{x: 12}]
deepcopy(ld)->map((_, v) => extend(v, {y: 34}))
echo ld
```
    [{'x': 12]
         ✔

But not if you just *replace* the items:
```vim
vim9script
var ld = [{x: 12}]
mapnew(ld, () => 0)
echo ld
```
    [{'x': 12]
         ✔

### `v:none` can be useful as a kind of sentinel value

For example, if you want to check the existence of a buffer-local variable in an
inactive buffer, you can't write this:

              ✘
       v--------------v
    if exists('b:name')
        ...
    endif

But you could write this:

                                      ✔
                              v---------------v
    if getbufvar(123, 'name', v:none) != v:none
        ...
    endif

See: <https://vi.stackexchange.com/a/28366/17449>

---

A sentinel value makes it possible to detect the end of some data.
For it to work as intended, its value must be invalid for the data.

In the  previous example,  I don't  think `v:none` is  really a  sentinel value,
because it's not used to detect the *end* of some data, but its *existence*.
But the usage is similar, so I guess it's close enough.

See: <https://en.wikipedia.org/wiki/Sentinel_value>

### when we filter a list, for some conditions, we may need to make a copy of the list

As an example, suppose that you want to filter this list:

    ['a', 'foo', '%', 'b', 'bar', '%', 'c']

And you  want to  remove 'foo'  and 'bar',  not because  of their  contents, but
because the next item is '%'.

You could naively run this:

    fu Func() abort
        let list = ['a', 'foo', '%', 'b', 'bar', '%', 'c']
        call filter(list, {i,_ -> get(list, i+1, '') isnot# '%'})
        echo list
    endfu
    call Func()
    ['a', '%', 'bar', '%', 'c']~

But it doesn't work as expected, because 'b' has been wrongly removed, and 'bar'
has not been removed.

---

The issue  is due  to the condition  which involves the  item following  the one
currently filtered;  and because `filter()` alters  the size of the  list during
the filtering.

Indeed, whenever `filter()` removes one item  from the list, the indexes of each
following item should be decreased by one.
But that's  not what  happens; after  removing an item,  Vim doesn't  update the
indexes of the next ones:

    fu Func() abort
        let list = ['a', 'foo', '%', 'b', 'bar', '%', 'c']
        call filter(list,
            \ {i,_ -> (writefile(['index ' .. i .. ' | next index ' .. (i+1)], '/tmp/log', 'a') + 2)
            \ && get(list, i+1, '') isnot# '%'})
        echo list
    endfu
    call Func()

    $ cat /tmp/log
    index 0 | next index 1~
    index 1 | next index 2~
    index 2 | next index 3~
    index 3 | next index 4~
    index 4 | next index 5~
    index 5 | next index 6~
    index 6 | next index 7~

In  the original  example, after  removing 'foo',  `filter()` inspects  the next
item, whose index is `2`.
But in the new list without 'foo', the  item of index 2 is not '%' anymore, it's
'b'.

Bottom line: `filter()` doesn't iterate over  a fixed list of items; it iterates
over a fixed list of indexes.

---

The solution is to make the condition work on a *copy* of the list.

    fu Func() abort
        let list = ['a', 'foo', '%', 'b', 'bar', '%', 'c']
        let list_copy = copy(list)
        call filter(list, {i,_ -> get(list_copy, i+1, '') isnot# '%'})
        "                             ^-------^
        echo list
    endfu
    call Func()
    ['a', '%', 'b', '%', 'c']~

If the test involved the current item, there would be no need for `copy()`.

---

More generally, whenever  your condition inspects the previous or  next items of
the list, you should make a copy.

The only  case where  maybe it's  useless to make  a copy  is if  your condition
inspects the previous items, while `filter()` doesn't alter them.

If  you wonder  how `filter()`  could alter  the previous  items, remember  that
`insert()` can insert an item at any position in a list.

And if you  wonder why `filter()` *necessarily* alters the  next items, remember
that  its purpose  is to  remove items;  and when  it does  remove one  item, it
necessarily alters the next ones, because their indexes are not updated as we've
just seen before.

##
## Refactor our vimrc/plugins to make function calls with many arguments more readable.

Look at the `Function calls` section in this file; one of its questions is:
"How can I name them to make the code more readable?"

##
## ?

Study when a wildcard can match a dot.
I think `*` can match a dot in a `:e` or `:sp` command:
```vim
vim9script
writefile([], '/tmp/some.unique.name')
sil e /tmp/som*niqu*ame
echom expand('%:p')
bw!
sil sp /tmp/som*niqu*ame
echom expand('%:p')
```
    /tmp/some.unique.name
    /tmp/some.unique.name

But not in a `'wig'` setting.
And probably not in other contexts; from `:h file-searching`:

   > The file searching is currently used for the 'path', 'cdpath' and 'tags'
   > options, for |finddir()| and |findfile()|.  Other commands use |wildcards|
   > which is slightly different.
   >
   > ...
   >
   > The usage of '*' is quite simple: It matches 0 or more characters.  In a
   > search pattern this would be ".*".
   > **Note that the "." is not used for file searching.**

Update:  Wrong.

`*` can match a dot in `'wig'`:
```vim
vim9script
cd /tmp
set wig=*obj
writefile([], '/tmp/some.unique.obj')
feedkeys(':e some.unique' .. "\t", 'nt')
```
    :e some.unique

And in other contexts listed at `:h file-searching`:
```vim
vim9script
var path: string = '/tmp/so.me/long/path/to/a/dir'
mkdir(path, 'p')
&path = '/tmp/*/long'
set hidden
writefile(['TEST'], path .. '/file')
setline(1, 'path/to/a/dir/file')
feedkeys('gf', 'n')
```
Why did you write that `*` could not match a dot in `'wig'`?

## ?

    expand('$LANG')

Retourne la valeur de la variable d'environnement `$LANG` du shell courant.

Si la session Vim connaît déjà la  variable d'environnement, il n'y a pas besoin
d'appeler `expand()`: `:echo $LANG` fonctionnera.

Mais si elle ne la connaît pas, `expand()` permet de s'assurer qu'elle sera bien
développée.  Pour ce faire, elle lance un shell pour l'occasion.

---

`expand()` n'est pas limitée à des fichiers, elle peut développer:

   - des caractères spéciaux (`:h cmdline-special`)
   - des commandes shell
   - des globs
   - des variables d'environnement

## ?

                ┌ respecte 'su' et 'wig'
                │      ┌ résultat sous forme de liste et non de chaîne
                │      │
    expand('*', false, true)
    glob('*', false, true, true)
                           │
                           └ inclut tous les liens symboliques,
                             même ceux qui pointent sur des fichiers non-existants

Noms des fichiers / dossiers du cwd.

---

Si le dossier de travail est  vide, `expand()` retourne `'*'`, `glob()` retourne
`''`.  `glob()` est  donc  plus  fiable.  Ceci  est  une  propriété générale  de
`expand()`.  Qd  elle ne  parvient pas  à développer qch,  elle le  retourne tel
quel:

    echo expand('$FOOBAR')
    $FOOBAR~

---

                                                            *suffixes*
    For file name completion you can use the 'suffixes' option to set a priority
    between files with almost the same name.  If there are multiple matches,
    those files with an extension that is in the 'suffixes' option are ignored.
    The default is ".bak,~,.o,.h,.info,.swp,.obj", which means that files ending
    in ".bak", "~", ".o", ".h", ".info", ".swp" and ".obj" are sometimes ignored.

    An empty entry, two consecutive commas, match a file name that does not
    contain a ".", thus has no suffix.  This is useful to ignore "prog" and prefer
    "prog.c".

    Examples:

      pattern:	files:				match:	~
       test*	test.c test.h test.o		test.c
       test*	test.h test.o			test.h and test.o
       test*	test.i test.h test.c		test.i and test.c

    It is impossible to ignore suffixes with two dots.

    If there is more than one matching file (after ignoring the ones matching
    the 'suffixes' option) the first file name is inserted.  You can see that
    there is only one match when you type 'wildchar' twice and the completed
    match stays the same.  You can get to the other matches by entering
    'wildchar', CTRL-N or CTRL-P.  All files are included, also the ones with
    extensions matching the 'suffixes' option.

    To completely ignore files with some extension use 'wildignore'.

    To match only files that end at the end of the typed text append a "$".  For
    example, to match only files that end in ".c": >
            :e *.c$
    This will not match a file ending in ".cpp".  Without the "$" it does match.

    The old value of an option can be obtained by hitting 'wildchar' just after
    the '='.  For example, typing 'wildchar' after ":set dir=" will insert the
    current value of 'dir'.  This overrules file name completion for the options
    that take a file name.

## ?

    expand('**/README', false, true)
    glob('**/README', false, true, true)

Liste des  chemins vers des fichiers  README situés dans  le cwd ou l'un  de ses
sous-dossiers.

À nouveau,  si aucun  fichier n'est  trouvé, `expand()`  retourne `['**/README']`,
tandis que `glob()` retourne `[]`.  `glob()` est donc plus fiable.

## ?

    glob("`find . -name '*.conf' | grep input`", false, true, true)
    systemlist("find . -name '*.conf' | grep input")

Sortie de la commande shell:

    $ find . -name '*.conf' | grep input

Quelles différences? :

   - `glob()` ne retourne que des noms de fichier existants.
     Elle filtre tout ce qui n'est pas exactement un nom de fichier exact.
     Les messages d'erreurs sont donc supprimés.

   - `system()` aussi, mais ajoute un newline à la fin, ce qui fait qu'on a une
     ligne vide en bas du pager.

## ?

    globpath(&rtp, 'syntax/c.vim', v:false, v:true, v:true)

Le chemin relatif `syntax/c.vim` est ajouté en suffixe à chaque chemin absolu du
rtp.  Si  le résultat  correspond à  un fichier  existant, il  est ajouté  à une
liste.  `globpath()` retourne  la liste finale, une fois que  tous les chemins du
rtp ont été utilisés.

---

    globpath(&rtp, '**/README.txt', v:false, v:true, v:true)

Idem, sauf que  cette fois, le suffixe  contient un wildcard, qui  à chaque fois
est développé en une liste de 0, 1 ou plusieurs fichiers correspondant.

---

Plus  généralement, `globpath()`  attend  2 arguments,  tous  2 des  expressions
évaluées en chaînes:

   - la 1e doit stocker des chemins séparés par des virgules
   - la 2e un chemin relatif vers un fichier, incluant éventuellement des wildcards

---

`globpath()` is useful to get an overview of a type of files.
Vim filetype plugins, C syntax plugins, lua indent plugins, keymap files, ...

    echo globpath(&rtp, 'ftplugin/vim.vim')
    echo globpath(&rtp, 'syntax/c.vim')
    echo globpath(&rtp, 'indent/lua.vim')
    echo globpath(&rtp, 'keymap/*.vim')

##
##
##
##
##
# Nombres

How to represent an hexadecimal number?

Use the `0x` prefix:

    echo 0x9a
    154~

---

How to represent an octal number?

Use the `0o` prefix:

    echo 0o17
    15~

---

Why should I never prefix a number with `0` (unless followed by `o`, `x`, `z`)?

Because it's  too ambiguous.   It might  be parsed  as an  octal number  or not,
depending on various parameters:

    # decimal
    echo 019
    19~

    # octal
    echo 017
    15~

    # decimal
    scriptversion 4
    echo 017
    17~

    # octal
    scriptversion 2
    echo 017
    15~

    # decimal
    vim9script
    echo 017
    17~

---

    echo 5.45e3
    5450.0~

En notation exponentielle, il faut obligatoirement un point et un chiffre après.
Ainsi 5e10 n'est pas valide, mais 5.0e10 est valide.

    echo 15.45e-2
    0.1545~

# Let

    let

Affiche l'ensemble des variables actuellement définies.

---

    let list2 = list1

Affecter à la variable list1 la référence de list2.

On peut vérifier que list1 et list2 partagent la même référence via:

        :echo list2 is list1

Il est probable que pour Vim une donnée soit décomposée en 3 parties (comme dans un fs):

   - son nom (associé à une référence dans une sorte d'annuaire)
   - une référence (pointant vers l'adresse mémoire de la donnée)
   - la donnée elle-même

Il ne faut pas croire que dans la  commande qui précède, on a dupliqué la donnée
stockée dans list1.
On  a simplement  créé un  nouveau  nom pointant  vers la  référence d'une  même
donnée.
Ceci explique pourquoi  si on modifie un  item de list1, on modifie  par la même
occasion list2 ; car les 2 noms d'objets sont associés à la même donnée.
Et réciproquement, modifier list2 a pour effet de modifier aussi list1.

Pour  dupliquer la  liste  stockée  dans list1,  il  faut  utiliser la  fonction
`copy()` ou `deepcopy()`.

---

    let [var1, var2; rest] = mylist

Affecter à `var1` la valeur `mylist[0]`, à `var2` la valeur `mylist[1]`, et tous
les autres  items de  `mylist` à  la liste  rest utile  pour éviter  d'avoir une
erreur si la taille de `mylist` pourrait être plus grand que le nb de variables.

---

    let s:myflag = exists('s:myflag') ? !s:myflag : 1
    let s:myflag = !get(s:, 'myflag', 1)

Stocke 1 dans la variable `s:myflag` si elle vaut 0, 1 autrement.

L'affectation prend  en charge le  cas où `s:myflag`  n'a pas encore  de valeur.
`s:myflag`  peut  être utilisée  comme  un  flag booléen  permettant  d'exécuter
alternativement 2 actions différentes A, B, A, B... (toggle)

Utile pex, pour (dés)activer la mise en surbrillance d'un pattern via :match.

    let s:myflag = ...
    if s:myflag
        match /pattern/
    else
        match none
    endif

Si B n'est pas  une action fixe et dépend d'une valeur,  le précédent code n'est
plus suffisant.
Dans ce cas, au lieu  de tester si s:myflag vaut 0 ou 1,  on peut tester si elle
existe ou non et lui affecter la valeur dont dépend B.

Utile  pex,  pour  (dés)activer  la   mise  en  surbrillance  d'un  pattern  via
matchadd().
En effet,  cette fois, la  désactivation de la  mise en surbrillance  n'est plus
fixe (:match none), mais dépend d'un id (:call matchdelete(id)).

    if !exists('id')
        let id = matchadd('SpellBad', 'pattern')
    else
        call matchdelete(id)
        unlet id
    endif

L'existence/absence de id répond à la question:

    Qu'a-t-on fait la dernière fois, A ou B ?
    Et donc que faire à présent, B ou A ?

La valeur de id répond à la question:

    Comment faire B ?

Une alternative utilisant le 1er code serait:

    let s:myflag = exists('s:myflag') ? !s:myflag : 1
    if s:myflag
        let id = matchadd('SpellBad', 'pattern')
    else
        call matchdelete(id)
        unlet id    " facultatif
    endif

L'inconvénient de cette  2e version est qu'elle crée 2  variables au lieu d'une,
une pour le flag et une pour l'id.

##
# Fonctions
## Théorie

Il ne faut jamais créer 2 fichiers dont le chemin depuis un dossier `autoload/` est identique:

    ~/.vim/plugged/a_plugin/autoload/foo.vim
    ~/.vim/plugged/b_plugin/autoload/foo.vim

En effet, si on définit une fonction dans le 2e fichier:

    fu foo#bar()
        echo 'hello'
    endfu

Elle ne sera jamais trouvée:

    call foo#bar()
    E117: Unknown function: foo#bar~

... car Vim s'arrêtera de chercher  dès qu'il trouvera un fichier `foo.vim` dans
un dossier `autoload/` du rtp.

## Buffers

    Ajoute:

    ┌────────────────────────────────────────┬───────────────────────────────────────────────────────────────────┐
    │ append('$', 'THE END')                 │ la ligne "THE END" après la dernière ligne du buffer courant      │
    ├────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
    │ append('.', '')                        │ une ligne vide après la ligne courante                            │
    ├────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
    │ append(0, ['Chapter 1', 'some title']) │ les lignes "Chapter 1" et "some title" au début du buffer courant │
    └────────────────────────────────────────┴───────────────────────────────────────────────────────────────────┘

    Teste l'existence d'un buffer dont:

    ┌─────────────────────────────────┬────────────────────────────────┐
    │ bufexists(42)                   │ le n° est '2                   │
    ├─────────────────────────────────┼────────────────────────────────┤
    │ bufexists('foo')                │ le nom est 'foo'               │
    ├─────────────────────────────────┼────────────────────────────────┤
    │ expand('~/.vimrc')->bufexists() │ le nom est '/home/user/.vimrc' │
    └─────────────────────────────────┴────────────────────────────────┘

            On peut utiliser un chemin absolu ou relatif par rapport au cwd.
            Mais si on utilise un chemin absolu, il ne doit pas contenir le tilde du home.
            Il faut développer ce dernier via expand().


    Teste l'existence d'un buffer listé et dont:

    ┌──────────────────┬──────────────────┐
    │ buflisted(3)     │ le n° est 3      │
    ├──────────────────┼──────────────────┤
    │ buflisted('foo') │ le nom est 'foo' │
    └──────────────────┴──────────────────┘


    Nom du:
    ┌────────────────┬───────────────────────────────────────┐
    │ bufname('%')   │ buffer courant                        │
    ├────────────────┼───────────────────────────────────────┤
    │ bufname('#')   │ alternate buffer                      │
    ├────────────────┼───────────────────────────────────────┤
    │ bufname('$')   │ dernier buffer                        │
    ├────────────────┼───────────────────────────────────────┤
    │ bufname(3)     │ buffer n° 3                           │
    ├────────────────┼───────────────────────────────────────┤
    │ bufname('foo') │ buffer contenant 'foo' (dans son nom) │
    └────────────────┴───────────────────────────────────────┘


    if !bufname('%')->empty()

            Teste si le buffer courant a bien un nom.


    Retourne le n° du buffer:
    ┌──────────────┬────────────────────────────┐
    │ bufnr('%')   │ courant                    │
    ├──────────────┼────────────────────────────┤
    │ bufnr('#')   │ alternate                  │
    ├──────────────┼────────────────────────────┤
    │ bufnr('$')   │ dernier de la liste        │
    ├──────────────┼────────────────────────────┤
    │ bufnr('foo') │ dont le nom contient 'foo' │
    └──────────────┴────────────────────────────┘

            En cas d'échec, retourne -1, et non 0.


    col('.')

            Byte index du caractère après le curseur, ou dit autrement:

                    - l'index du 1er octet du caractère qui suit le curseur
                    - le poids de la chaîne allant du début de la ligne jusqu'au curseur, +1

                      Pk +1?
                      Sans doute car `0` est réservé pour une erreur.

            Exemple:

                fooé|bar    foo étant au début d'une ligne et le curseur étant représenté par le pipe,
                            col('.') retourne 6

                            Du début de la ligne jusqu'au curseur, il y a 5 octets (dans 'fooé', 'é' en pèse 2),
                            l'octet suivant est donc le 6e.


    col('$')

            Poids de la ligne + 1.
            Index de l'octet imaginaire suivant le dernier caractère sur la ligne.


    getbufvar('%', '')

            Dictionnaire contenant toutes les variables locales au buffer courant ainsi que leurs valeurs.

            getbufvar() permet d'accéder à la valeur d'une variable ou option locale à un buffer.
            Ne fonctionne pas pour une option locale à une fenêtre (utiliser getwinvar() pour ça).


    getbufvar('%', '&ft')
    getbufvar(5, 'myvar', 'default')

            Type de fichier du buffer courant
            Valeur de `b:myvar` dans le buffer n° 5, si elle existe; 'default' autrement.


    Contenu de la ligne:

    ┌──────────────┬────────────────────────┐
    │ getline(123) │ dont l'adresse est 123 │
    ├──────────────┼────────────────────────┤
    │ ...('$')     │ à la fin du buffer     │
    ├──────────────┼────────────────────────┤
    │ ...("'a")    │ portant la marque a    │
    ├──────────────┼────────────────────────┤
    │ ...('w0')    │ en haut de la fenêtre  │
    ├──────────────┼────────────────────────┤
    │ ...('w$')    │ en bas de la fenêtre   │
    └──────────────┴────────────────────────┘

    Retourne le n° de la ligne:

    ┌───────────┬───────────────────────┐
    │ line('$') │ en bas du buffer      │
    ├───────────┼───────────────────────┤
    │ ...("'a") │ portant la marque a   │
    ├───────────┼───────────────────────┤
    │ ...('w0') │ en haut de la fenêtre │
    ├───────────┼───────────────────────┤
    │ ...('w$') │ en bas de la fenêtre  │
    └───────────┴───────────────────────┘

    line2byte(42)

            retourne le poids en octets du buffer courant depuis son début jusqu'à la fin de la ligne 41
            (les newlines sont inclus)


    line2byte(line('$') + 1)

            retourne le poids total en octets du buffer courant + 1

            Cette expression est utile pour vérifier qu'un buffer est vide de contenu:

                    if line2byte(line('$') + 1) <= 2
                    ...

            Pk `line('$') + 1` et pas `line('$')` tout court?
            Parce que `line('$')->line2byte()` retournerait le poids en octets depuis le début du buffer
            jusqu'à la fin de l'avant-dernière ligne, et non pas jusqu'à la fin de la dernière ligne.

            Ainsi, si le buffer contient une seule ligne et qu'elle est non vide, cette expression
            retournera 1.
            Ce `1` signifie sans doute qu'un buffer contient au moins un octet avant tout texte
            (peut-être le BOM = Byte Order Mark ?).
            Et comme `1 <= 2`, le test passera alors qu'il ne devrait pas puisque le buffer est non vide.

            Pk `<= 2`?
            Parce qu'une ligne vide contiendra au moins un 1er caractère (BOM?) et un newline à la fin.

## Diverses

    inoremap <F2> <C-R>=CustomMenu()<cr>
    fu CustomMenu()
        call complete(col('.'), ['foo', 'bar', 'baz'])
        return ''
    endfu

            Ce bout de code montre comment utiliser la fonction complete() pour se créer un menu
            de complétion custom.
            Ici, en appuyant sur <F2>, un menu dont les items sont foo, bar et baz s'affichera.

            Le 1er argument précise à partir d'où l'item choisi sera inséré sur la ligne.
            On pourrait lui donner comme valeur:

                    - col('.')

                            ne remplace rien; insertion à partir du curseur

                    - col('.') - 3

                            remplace les 3 derniers caractères

                    - col('.') - getline('.')[: col('.') - 2]->matchstr('\S\+$')->strlen()

                            remplace le texte devant le curseur;
                            le texte étant défini comme une séquence de non-whitespace

            Bien sûr, la fonction CustomMenu() pourrait utiliser/construire n'importe quelle liste
            contenant les items qu'on souhaite pouvoir insérer automatiquement.
            Pex, la liste des contenus des registres.

            Toutefois, si ceux-ci contiennent des LF, le menu les traduit en NUL.
            Peut-être car `complete()` n'est pas censée accueillir des items multilignes.

            On notera également l'instruction return '' qui est nécessaire pour éviter que `CustomMenu()`
            ne retourne le code de sortie 0 qui serait alors automatiquement inséré à la suite du 1er
            item (foo0), sans que le menu ne s'affiche.


    confirm('Are you sure?', "&yes\n&no\n&quit", 2)

            Affiche une ligne affichant le message 'Are you sure?', propose à l'utilisateur
            un choix entre 'yes', 'no' et 'quit', attend  que l'utilisateur tape 'y', 'n' ou 'q'
            et retourne le n° du choix.
            Le choix par défaut, si on appuie seulement sur Enter, est 'no' (3e argument: 2).

            Les choix doivent être séparés par des \n.
            Pour un choix donné, on peut choisir quelle lettre permet de le sélectionner en la faisant
            précéder de &.
            Retourne 0 si l'utilisateur appuie sur C-c ou Esc.


    let password = inputsecret('Enter sudo password:') .. "\n"
    echo system('sudo -S aptitude install package', password)

            inputsecret() est similaire à input() à ceci près que les caractères tapés sont affichés
            sous la forme d'astérisques, et que la saisie n'est pas sauvegardée dans l'historique:
            histget('@')

            `system()` écrit sur l'entrée standard de `sudo`.

            Pb:          par défaut, `sudo` ne lit pas son entrée standard, mais le terminal.
            Solution:    utiliser le flag `-S` (--stdin)
                         Ce flage demande à `sudo` qu'il lise le mdp sur son entrée standard,
                         et qu'il écrive son prompt sur l'erreur standard.

            Le mdp doit être suivi d'un newline (sans doute pour valider).
            En pratique, ça a l'air de fonctionner même sans newline à la fin.

            On pourrait simplement `:call` la fonction `system()`, mais en utilisant `:echo`,
            on peut lire la sortie de la commande shell et ainsi vérifier que l'installation
            du paquet s'est bien passée.

                                               NOTE:

            En pratique, il vaut mieux éviter ces commandes, car on ne peut pas répondre à d'éventuelles
            questions au cours de l'installation (pex pour résoudre des pbs de dépendances).


    let choice = inputlist(['Select color:', '1. red', '2. green', '3. blue'])
    if choice >= 1 && choice <= 3
        let color  = ['red', 'green', 'blue'][choice - 1]
    endif

            stocke dans la variable `color` un des items de la liste ['red', 'green', 'blue'],
            choisi via un menu interactif

            Dans l'exemple précédent, si l'utilisateur veut choisir la couleur verte, il entrera le nb 2.
            Du coup on obtiendra:

                    let color = ['red', 'green', 'blue'][2-1] = 'green'

            Il peut être utile de mettre un prompt comme 1er item (ou alors faire un :echo 'message' avant),
            et de préfixer les autres par un nb pour que l'utilisateur sache exactement quoi taper.

            La taille de la liste passée en argument à inputlist() et ce qu'elle contient n'a pas d'importance,
            elle ne sert qu'à informer l'utilisateur des nb qu'il peut taper et leur conséquence.


    taglist('pattern')

            Retourne la liste des tags matchant pattern.

            Chaque item de la liste est un dictionnaire, contenant entre autres les clés `name` et `filename`.


    taglist('pattern')[0].name
    taglist('pattern')[0].filename
    taglist('pattern')->map('v:val.name')

            retourne le nom:

                    - du 1er tag                         matchant pattern
                    - du fichier contenant le 1er tag    "
                    - des noms de tous les tags          "

## Fenêtres / Onglets

    getwinvar('%', '')

            retourne un dictionnaire contenant toutes les variables locales à la fenêtre courante
            ainsi que leurs valeurs

            `getwinvar()` permet d'accéder à la valeur d'une variable ou option locale à une fenêtre.
            Ne fonctionne pas pour une option locale à un buffer (utiliser getbufvar() pour ça).

                                     TODO:

            Parler de `gettabwinvar()` qui permet aussi d'obtenir une variable locale à une fenêtre
            mais pas forcément dans l'onglet courant (dans celui de son choix).
            Parler aussi de `gettabvar()` pour obtenir une variable locale à un onglet.

            Parler aussi de `getwininfo()`.


    bufwinnr('%')
    bufwinnr('#')
    bufwinnr('$')
    bufwinnr(3)

            Retourne le n° de la 1e fenêtre dans l'onglet courant qui affiche:

                    - le buffer courant
                    - l'alternate buffer
                    - le dernier buffer listé
                    - le buffer n° 3

            Si le buffer n'existe pas ou n'est affiché dans aucune fenêtre de l'onglet courant,
            -1 est retourné.


    if bufwinnr(42) > 0

            Teste si le buffer n°42 est affiché dans une fenêtre de l'onglet courant.


    if !win_findbuf(42)->empty()

            Teste si le buffer n°42 est affiché dans une fenêtre qcq (dans n'importe quel onglet).

            `win_findbuf(42)` retourne une liste d'identifiants de fenêtres affichant le buffer n°42.


    win_getid()
    win_getid([2])
    win_getid([4, 3])

            Retourne l'id de la:

                    - fenêtre courante
                    - 2e fenêtre de l'onglet courant
                    - 3e fenêtre du 4e onglet

            L'id d'une fenêtre est absolu, contrairement à son n° (donné par `winnr()`) qui lui est
            local à l'onglet.


    call win_gotoid(42)
         win_id2win(42)
         win_id2tabwin(42)

            donne le focus                      à la fenêtre d'id 42
            retourne le n° (!= id)              de la "
            retourne la liste [tabnr, winnr]    "

            `win_id2win()` ne retourne le n° de la fenêtre que si on se trouve dans son onglet.
            Autrement, elle retourne 0.


    win_getid(1, 1)

            retourne l'id de la fenêtre de n° 1 dans l'onglet 1


    winnr()
    winnr('#')
    winnr('$')

            retourne le n° de:

                    - la fenêtre courante
                    - la dernière fenêtre visitée
                    - la dernière fenêtre de l'onglet courant

            Le n° est local à l'onglet.

                                               NOTE:

            On remarque que le caractère spécial # n'a pas le même sens pour winnr() et bufwinnr().
            Pour winnr() il s'agit de la dernière fenêtre visitée, et pour bufwinnr() celle affichant
            l'alternate buffer.

            De même, $ est interprété comme la dernière fenêtre par winnr(), mais comme le dernier buffer
            listé par bufwinnr().

            Enfin, `winnr() != bufwinnr('%')`, car:

                    - winnr()    = n° de la fenêtre courante
                    - bufwinnr() = n° de la 1e fenêtre affichant le buffer courant

                                     TODO:

            Parler aussi de tabpagenr() qui fait qch de similaire: retourner le n° d'un onglet.
            À ceci près qu'il n'accepte pas '#' comme argument; soit rien, soit '$':

                    tabpagenr()       n° onglet courant
                    tabpagenr('$')    n° dernier onglet

            Parler aussi de tabpagewinnr(): retourne le n° d'une fenêtre dans un onglet de son choix.


    @=winnr('#') CR C-w c         mode normal
    :exe winnr('#') .. 'close'    mode Ex

            Fermer la dernière fenêtre qu'on a visité dans l'onglet courant.


    call winrestview(view)

            restaure l'état de la fenêtre à partir des informations du dictionnaire stocké dans `view`
            et peuplé par `winsaveview()`

                                               NOTE:

            Si la partie du buffer affichée par la fenêtre est pliée, avant d'utiliser cette fonction,
            il faut la déplier (`:norm! zv`).

            Autrement, la position de la ligne courante au sein de la fenêtre est perdue, car Vim
            la positionne au centre de cette dernière peu importe sa position d'origine
            (en haut/bas de la fenêtre ...).

            Le pb vient du fait que winsaveview() ne sauvegarde pas les informations relatives au pliage.

## Fichiers

    delete(fname)

            supprime le fichier `fname`

            Retourne 0 si la suppression a réussie, -1 autrement.

    delete(dir, 'd')

            supprime le dossier `dir`

            Échoue si `dir` n'est pas vide.

    delete(dir, 'rf')

            supprime le dossier `dir` et tout ce qu'il contient, récursivement

            Un lien symbolique est supprimé, mais pas ce sur quoi il pointe.


    if !glob('/path/to/file')->empty()

            teste L'EXISTENCE de /path/to/file (fonctionne même si on n'a pas les droits pour le lire)

            Ce test peut s'écrire simplement comme ça car le code de retour de empty()
            en cas d'échec est 0.  Si c'était -1, il faudrait obligatoirement comparer la sortie à -1.

            Pour tester l'existence d'un fichier, il faut utiliser cette syntaxe, et non `filereadable()`.


    fnamemodify('fname', ':p:h')

            Retourne le chemin absolu vers le dossier contenant le fichier fname.

            Où la fonction cherche-t-elle le dossier contenant fname ?
            Probablement dans les dossiers de 'path'.

            Cette fonction permet de modifier le nom d'un fichier/dossier à partir de certains
            modificateurs dont la liste est lisible via :h filename-modifiers.
            Les plus utiles sont:

            ┌──────────────┬────────────────────────────────────────────────────────────────────────────┐
            │ :~           │ preserve home                                                              │
            │              │ ne développe pas ~; doit être utilisé avant les autres                     │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :.           │ réduit le chemin de sorte qu'il soit relatif au cwd                        │
            │              │ si c'est possible càd si le fichier courant est sous le cwd                │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :~:.         │ chemin réduit au max                                                       │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :h           │ chemin relatif au cwd, sans le dernier noeud                               │
            │              │ répétable (ex:  :h:h  pour obtenir le dossier du dossier)                  │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :t           │ fichier                                                                    │
            │              │ complément de :h                                                           │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :e           │ extension                                                                  │
            │              │ répétable (ex:  :e:e  pour obtenir les 2 dernières extensions)             │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :r           │ supprime l'éventuelle extension du fichier +   chemin relatif au cwd       │
            │ :p:r         │                                                chemin absolu               │
            │ :t:r         │                                                pas de chemin               │
            │              │                                                                            │
            │              │ répétable, ex:  :r:r  →  supprime les 2 dernières extensions               │
            │              │ complément de :e                                                           │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :e:e:r       │ avant-dernière extension                                                   │
            │              │                                                                            │
            │              │ ex:  e foo.tar.gz                                                          │
            │              │      expand('%:e:e:r')  →  tar                                             │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :p           │ chemin absolu complet                                                      │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :S           │ escape special characters for use with a shell command                     │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :s?pat?sub?  │ substitue la 1e occurrence de pat par sub                                  │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :gs?pat?sub? │ substitue toutes les occurrences de pat par sub                            │
            └──────────────┴────────────────────────────────────────────────────────────────────────────┘


    fnamemodify(myvar, ':p')

            Retourne le chemin complet vers le fichier/dossier dont le chemin est stocké dans `myvar`.

            La fonction expand() permet aussi de modifier des noms de fichiers mais uniquement ceux
            exprimés via des caractères spéciaux (%, #, <cfile>).

            fnamemodify() est donc + puissante, elle peut même agir sur des noms de fichiers inexistants.
            Ex:

                    :echo fnamemodify('UnexistingFile', ':p')

            ... marche même si `UnexistingFile` n'existe pas.


    echo fnamemodify('/foo/bar/baz/', ':t')
    ''~
    echo fnamemodify('/foo/bar/baz/', ':h:t')
    baz~
    echo fnamemodify('/foo/bar/baz', ':t')
    baz~

            `:h` removes the last path component.
            But the last path component can be empty, if the last character of the path is `/`.


    :exe 'e ' .. fnameescape('fname')

            Exécute la commande  Ex ':edit fname' en ayant  échappé les symboles
            spéciaux que fname contient.
            Si  fname contient  un %  ou un  |, ça  permet d'éviter  que Vim  ne
            développe ces symboles.


    !isdirectory(expand('$HOME') .. '/dir')

            teste la non-existence du dossier /home/user/dir

            Ce test peut s'écrire simplement comme ça car le code de retour de isdirectory()
            en cas d'échec est 0.  Si c'était -1, il faudrait obligatoirement comparer la sortie à -1.


    readfile('/tmp/foo')
    readfile(fname, '', 10)
    readfile(fname, '', -10)

            Retourne une liste dont les items sont des lignes du fichier `/tmp/foo`:

                    - toutes
                    - les 10 premières
                    - les 10 dernières


    let words = readfile('/tmp/foo')->join("\n")->split('\W\+')

            stocke dans la variable words une liste contenant le 1er mot de chaque ligne du fichier /tmp/foo

            Ceci illustre comment on peut utiliser la fonction split() pour récupérer toutes les occurrences
            d'un pattern.  Ne fonctionne que si on peut facilement décrire l'inverse du pattern.
            Ici on cherche des mots (\w\+), l'inverse est donc facile à décrire \W\+.

            On aurait aussi pu utiliser:    [^a-zA-Z_0-9\d192-\d255]
            Pour trouver des mots dont les caractères sont présents dans 'isk'.


    shellescape(fname, 1)

            protège un nom de fichier qui doit être passé en argument à une commande shell

            La protection consiste à mettre des single quotes autour de fname et à échapper d'éventuels
            single quotes si fname en contient.

            Qd le 2e argument optionnel est non nul, les symboles appartenant à [!%#<] sont échappés.
            Lorsque `shellescape(fname, 1)` sera envoyée au shell, via :! ou :grep,
            sur la ligne de commande Ex, Vim enlèvera les backslashs sans développer les caractères
            spéciaux.

                                               NOTE:

            La règle à retenir est la suivante:

            Qd on veut protéger des caractères spéciaux:

                    - de Vim,             il faut utiliser `fnameescape(...)`
                    - du shell,           "                `shelleescape(...)`
                    - du shell ET de Vim, "                `shellescape(..., 1)`

                                               NOTE:

            `fname` pourrait être autre chose qu'un nom de fichier: pex un nb en hexa
            (commençant donc par un dièse), qu'on souhaite passer à une commande shell:

                    exe '!shell_cmd ' .. shellescape('#' .. l:mycolor, 1)


    :let @" = 'foo;ls'     | exe 'grep! '.shellescape(@",1) .. ' .'
    :let @" = "that's"     | ...
    :let @" = 'foo%bar'    | ...

            Même si `:grep` est une commande Vim, qd on lui passe une chaîne pouvant contenir
            des caractères spéciaux, il faut utiliser `shellescape()`, et PAS `fnameescape()`.

            Voici la sortie de différentes fonctions, suivant le contenu du registre `z`:

                    ┌───────────────────┬──────────┬─────────────┬────────────┐
                    │                   │ foo;ls   │ that's      │ foo%bar    │
                    ├───────────────────┼──────────┼─────────────┼────────────┤
                    │ fnameescape(@")   │ foo;ls   │ that\'s     │ foo\%bar   │
                    │ shellescape(@")   │ 'foo;ls' │ 'that'\''s' │ 'foo%bar'  │
                    │ shellescape(@",1) │ 'foo;ls' │ 'that'\''s' │ 'foo\%bar' │
                    └───────────────────┴──────────┴─────────────┴────────────┘

            On remarque que `fnameescape()` ne protègerait pas `;`.
            Le shell l'interprèterait comme une fin de commande, et exécuterait le reste
            comme s'il s'agissait d'une autre commande.
            C'est DANGEREUX.
            Imaginons que `@"` contienne la chaîne suivante:

                    foo;rm -rf

            Au lieu de chercher "foo;rm -rf", le shell exécuterait `$ grep foo`, PUIS `rm -rf`.


    system('chmod +x -- ' .. expand('%')->shellescape())

            retourne la sortie de la commande shell:

                    $ chmod +x -- 'foo bar'

            'foo bar' étant le nom du buffer courant

                                               NOTE:

            Il existe 2 différences entre les syntaxes:

                    :!exe {expr}
            et
                    :call system({expr})


            - system() permet de capturer la sortie du shell dans une variable ou de la passer
              à une autre commande Vim

            - system() ne lance pas de terminal, elle passe la commande shell directement à un processus
              shell;    :!exe    lance un émulateur de terminal au sein duquel tourne un shell

              Ceci peut avoir son importance si on a besoin d'interagir avec la commande shell.
              C'est le cas pex avec le pgm ranger (file manager).
              On ne peut pas le lancer via system(), car dans ce cas ranger se plaindrait qu'il
              a besoin d'être exécuté depuis un terminal.


    tempname()
    let tmpfile = tempname()

            Retourne / capture le nom d'un fichier temporaire.  Ex:

                    /tmp/abcd123/0

            Le dossier le contenant est automatiquement créé dans les 2 cas.


                                               NOTE:

            Le simple fait d'invoquer la commande shell `mktemp` provoque également la création d'un
            dossier temporaire par Vim:

                    call system('mktemp -d /tmp/.pgm.XXXXXXXXXX')
                    /tmp/abcd123/ + /tmp/.pgm.abcdef12345~

            Toutefois, on préfèrera utiliser `tempname()`, car qd on le réinvoquera, Vim créera tous
            les fichiers suivants dans le même dossier.
            De plus, qd on quittera Vim, il supprimera automatiquement le dossier.

## Historique

    strftime('%c')->histadd('/')

            ajouter dans l'historique de recherche la date du jour

                                               NOTE:

            Il existe d'autres historiques qu'on peut manipuler via histadd(), histdel(), histget() et histnr():

                : ou cmd       ligne de commande
                / ou search    recherche
                = ou expr      registre expression
                @ ou input     dernières valeurs fournies à la fonction input()
                > ou debug     commandes de déboguage

    histdel('/')
    histdel('/', -1)
    histdel('/', '^a.*b$')

            supprimer de l'historique de recherche:

                    - toutes les entrées
                    - la dernière entrée
                    - toutes les entrées commençant par a et finissant par b

    histget('/', 5)
    histget('/')

            retourne la 5e entrée de l'historique de recherche; la dernière entrée

                                               NOTE:

            - on peut fournir un n° d'index absolu (nb positif), ou relatif par rapport à la fin
              (nb négatif, -1 = dernière entrée)

            - l'index absolu d'une entrée dans l'historique de recherche ne correspond pas forcément
              au n° de la ligne sur laquelle il est présent dans la fenêtre qui pop via q/

    histnr('/')

            retourne le n° d'index de la dernière entrée dans l'historique de recherche


    " search something
    call histdel('/', -1)
    let @/ = histget('/')

            supprime la dernière recherche, et restocke dans le registre recherche l'avant-dernière
            utile après une recherche dont on ne souhaite laisser aucune trace (ou alors utiliser :keeppatterns)

## Recherche

What's the use of the `z` flag for `search()`?

It seems that if we omit it, Vim does the same thing:

   > When the 'z' flag is not given, searching always starts in
   > column zero **and then matches before the cursor are skipped**.

If the  matches before the  cursor are skipped,  then why bother  searching from
column zero?

Answer: Its purpose might be to increase performance.
Even if  searching from column 0,  then ignoring the matches  before the cursor,
gives the same result as searching from the cursor, it costs more time.

See also:

   - <https://github.com/vim/vim/issues/6572#issuecomment-666670144>
   - <https://vi.stackexchange.com/questions/29489/what-does-the-z-flag-for-search-do>

