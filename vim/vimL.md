# vim-vint
## How to install it?

    $ git clone https://github.com/Kuniwak/vint
    $ cd !$:t
    $ python3 -m pip install --user --upgrade .

    $ cd ..

    $ git clone https://github.com/pypa/setuptools_scm
    $ cd !$:t
    $ python3 -m pip install --user --upgrade .

##
# Function calls
## I have a function call with many arguments
### how to make it more readable?

Break the arguments on multiple lines:

    call Func(
        \ arg1,
        \ arg2,
        \ ...
        \ )

This kind of syntax is probably portable across many other programming languages
(C, python, ...).

### how to reduce their number (knowing that some of them can be derived from a single expression)?

Pass the expression from which some of the arguments can be derived, and let the
function compute the arguments inside its body.

Example:

    let view = winsaveview()
    call Func(lnum, col)
              ^^^^^^^^^
              2 arguments

    →

    let view = winsaveview()
    call Func(view)
              ^^^^
              1 argument

    fu Func(view)
        let [lnum, col] = [a:view.lnum, a:view.col]
    endfu

##
## How to avoid
### passing the same argument(s) in several calls to the same function?

Use a partial:

    fu Func(a, b, ...)
        if a:0
            echom printf('received 4 arguments: %d, %d, %d, %d', a:a, a:b, a:1, a:2)
        else
            echom printf('received 2 arguments: %d, %d', a:a, a:b)
        endif
    endfu
    let b:partial = function('Func', [1, 2])

Now you can make those 2 function calls:

    call b:partial()
    call b:partial(3, 4)

---

Without a partial, you would had to write:

    call Func(1, 2)
    call Func(1, 2, 3, 4)

Note that  we used  `b:` here to  make the example  easily reproducible,  but in
practice,  you'll  probably make  your  function  calls  inside  the body  of  a
function; in which  case, you can use  `l:` instead, but you  need to capitalize
the name of the partial:

    let l:Partial = function('Func', [1, 2])
        ^^^

---

Analogy: Just like you can tattoo some  drawing(s) on a person, you can "tattoo"
arguments on a function; it then becomes a partial.

### passing the same arguments in several calls to different functions?

Assign them to a list, and pass the latter to the function with `call()`:

    let args = [1, 2, 3]
    call call('FuncA', args)
    call call('FuncB', args)
    ...
    fu FuncA()
        let [a, b, c] = a:000
    endfu


Without `call()`, you would had to write:

    call FuncA(1, 2, 3)
    call FuncB(1, 2, 3)
    ...

---

Btw, `call()` is useful even if there are non-repeating arguments before/after:

    let args = [1, 2, 3]
    call call('FuncA', args + [4, 5])
    call call('FuncB', [6, 7] + args)
    ...
    fu FuncA()
        let [a, b, c] = a:000
    endfu

---

Analogy: Just like you can put several  drawings inside a packaging to send them
to a person, you can "package" arguments in a list and pass it to a function via
`call()`.

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
## What are the pros of using `:put =` over `append()` or `setline()`?

`:put =`  is more handy  on the command-line,  in an interactive  usage, because
less verbose.

Also, it moves the cursor on the last line pasted.
This is handy when you have multiple blocks of text to paste.

With `append()` and `setline()`, you would have to re-compute the line address
from which you want to paste every block, to avoid that they overlap.

## What are the cons of using `:put =`?

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

## What happens if I execute `:put =['foo', 'bar']` in a new buffer?  What's the difference with the previous `append()`?

Like with the previous `append()`, you get an empty line, 'foo', then 'bar'.
Unlike the previous `append()`, the cursor moves on the 'bar' line.

###
## How to use `append()` and make the cursor move like `:put =`?

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
            ^^^^^^^^^^^^^^^^^^^^^

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
# Antipatterns
## When can I simplify `empty(filter(...))`?

When the condition passed to `filter()` is a simple regex or string comparison.

### How to simplify it?

Use `index(...) == -1` or `match(...) == -1`.

If the test is inverted by a bang, then replace `== -1` with `>= 0`.

---

For example, to express that a list contains an item matching a pattern, write this:

    match(list, pat) >= 0

and not this:

    !empty(filter(copy(list), {_,v -> v =~# pat}))

---

As another example, to express that there's no location window anywhere, write this:

    index(map(getwininfo(), {_,v -> v.loclist}), 1) == -1

and not this:

    !empty(filter(map(getwininfo(), {_,v -> v.loclist}), {_,v -> v}))

You could even write:

    match(getwininfo(), "'loclist': 1") == -1

This works  because each item in  the output of `getwininfo()`  is a dictionary,
and in that case `match()` uses a dictionary as a string.

Although, it feels awkward and brittle...
What  if one  day the  output of  `getwininfo()` uses  double quote  to surround
`loclist`, or adds/removes a space after `:`?
You would need a more permissive pattern.

#### Why should I do it?

It's shorter, and thus a little more readable.

There's  less risk  of an  unexpected side-effect;  indeed, `filter()`  operates
in-place, which often requires you not to forget to use `copy()` or `deepcopy()`.

#### When is such a simplification impossible?

When the condition passed  to `filter()` is more complex than  a simple regex or
string comparison:

    empty(filter(copy(list), {_,v -> v.foo == 1 && v.bar != 2}))
                                     ^^^^^^^^^^^^^^^^^^^^^^^^
                                     assume that `list` contains dictionaries with the keys `foo` and `bar`

##
## The next expression uses a ternary conditional:

    var is# 'foo'
    \ ?     1
    \ : var is# 'bar'
    \ ?     2
    \ :     3

### How should I rewrite it?

    {'foo': 1, 'bar': 2, 'baz': 3}[var]

Or:

    get({'foo': 1, 'bar': 2}, var, 3)

---

Use the first expression if you know the third value which can be assigned to `var`.
Use the second one if you don't know what other value(s) can be assigned to `var`.

#### Why?

  - more concise/readable

  - mentions explicitly the third value `baz` in the first case
    (before it was implicit/not mentioned at all)

  - easier to expand later if `var` can have more values

##
# Miscellaneous
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
## How can the following assignment be simplified?

    let test = var == 123 ? 1 : 0
↣
    let test = var == 123
↢

### Why is it possible?

A  comparison  is an  expression,  whose  value is  `1`  when  it succeeds,  `0`
otherwise; as such, it can be used (alone) in the rhs of an assignment.

    let var = 123
    let test = var == 123
    echo test
    1~

##
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
For example, run this command:

    $ vim -Nu <(cat <<'EOF'
    pu! =join(map(range(97, 122), {_,v -> nr2char(v)}), '')
    t.
    call setpos('.', [bufnr(), line('.'), col('.'), 0, 12])
    norm! k
    EOF
    )

Notice that the  `k` motion has made  the cursor move onto the  character `l` of
the first  line of text;  this is because `setpos()`  has set `curswant`  to the
value 12, and `l` is the 12th character on the line.

##
## How to get the command with which Vim was started?

        :echo system('ps -o command= -p '.getpid())

Useful  if you  want to  parse the  command-line to  install some  configuration
depending on the flags which were passed to Vim on the shell's command-line.

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

## How to get the path to the parent of
### a given file?

Use `fnamemodify()` and `:p:h`:

    echo fnamemodify($MYVIMRC, ':p:h')
    /home/user/.vim~

### a non-existing directory?

Use `fnamemodify()` and `:p:h`:

    echo fnamemodify($HOME . '/.vam', ':p:h')
    /home/user~

### an existing directory?

Use `fnamemodify()` and `:p:h:h`:

    echo fnamemodify($HOME . '/.vim', ':p:h:h')
    /home/user~

---

You  need two  `:h`  because `:p`  adds  a trailing  slash to  the  path if  the
directory exists.

    echo fnamemodify($HOME . '/.vim', ':p')
    /home/user/.vim/~
                   ^
    echo fnamemodify($HOME . '/.vam', ':p')
    /home/user/.vam~
                   ^

This has an effect on the `:h` modifier, because the latter considers a trailing
slash as a (empty) path component.

##
## When can I *not* add a comma after the last item of a list?

When the list is the left operand of an assignment (`:h :let-unpack`):

    let [a,b,c,] = [1,2,3]
    "         ^
    "         ✘
    E475: Invalid argument: ] = [1,2,3]~

## Why should I avoid using `matchend()` instead of `matchstr()->len()`?

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

##
## ?

How to play a sound?

Use `sound_playfile()` or `sound_playevent()`.

For example, you could download the intro music for the PlayStation 1:

    $ youtube-dl -x --audio-format vorbis -o 'ps.%(ext)s' 'https://www.youtube.com/watch?v=oAhvQoLpvsM'

Then, play it when Vim starts, adding this code to your vimrc:

    if ! has('nvim')
        augroup play_ps_sound_on_vimenter
            au!
            au VimEnter * call sound_playfile('/tmp/ps.ogg')
        augroup END
    endif

Note that you really need `%(ext)s` in  the value passed to the argument `-o` of
`youtube-dl(1)`; I think that's because the latter expects a template.
You could  write `ps.ogg` directly, and  `mpv(1)` would play the  file (although
with a warning message, I think), but not Vim.

---

The `complete` "event" is a nice and probably useful sound:

    call sound_playevent('complete')

As an example, it could be played after an async command has finished populating the qfl.

##
# Issues
## Why does  `:call system('grep -IRn pat * | grep -v garbage >file')`  fail to capture the standard error in file?

The pipe between the  two greps redirects only the standard  output of the first
grep, not its standard error.

If you really want the errors too, then group the commands:

    { grep -IRn pat * | grep -v garbage  ;} >file 2>&1
    ^                                    ^^

## ?

My function is slow.  It executes some `:norm` commands.  What can I do to improve the performance?

Check whether some of them enter insert mode.
If some  do, prefix them with  the `:noa` modifier to  prevent the `InsertEnter`
and `InsertLeave` events from being fired.

Remember  that replace  mode is  a submode  of insert  mode; so  if you  execute
`:norm` to replace a character, you probably want to prefix it with `:noa` too.

So far, it has helped us in `vim-breakdown` and in `comment#and_paste()`.

    cmd

##
# Todo
## Document the fact that when we filter a list, for some conditions, we may need to make a copy of the list.

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
            \ {i,_ -> (writefile(['index ' . i . ' | next index ' . (i+1)], '/tmp/log', 'a') + 2)
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
        "                             ^^^^^^^^^
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
##
##
# Expressions

Une expression peut être :

   - un nb
   - une chaîne
   - un dictionnaire
   - une variable
   - une variable d'environnement     préfixe $
   - une option                       préfixe &
   - un registre                      préfixe @
   - une expression conditionnelle    a ? b : c
   - la sortie d'une fonction
   - le résultat d'une opération entre 2 expressions (+, -, *, /, %, .)


        :let myvar42 = 'hello'
        :let idx=42
        :echo myvar{idx}

        :fu MyFunc42()
        :    return 'world'
        :endfu
        :let idx=42
        :echo MyFunc{idx}()

                On peut développer (interpoler?) une expression au sein même d'un nom de variable
                ou de fonction. Cf. :h curly-braces-names

                                               NOTE:

                Il peut s'agir d'une alternative à eval():

                        :let myvar42 = 'hello'
                        :let idx=42
                        :echo eval('myvar' . idx)

                        :fu MyFunc42()
                        :   return 'world'
                        :endfu
                        :let idx=42
                        :echo eval('MyFunc' . idx . '()')

                eval() est moins lisible:

                        :echo eval('myvar'.idx)
                        :echo myvar{idx}

                                     NOTE:


        It works even if there's nothing outside the curly braces:

                :let var = 'hello'
                :let {var} = 'world'
                :echo hello
                world ~


    system('ls -l ' . expand('%:p'))

            Une concaténation de chaînes étant une expression, on peut la passer directement en argument
            à une fonction.

            Pas besoin de:

                    system ("ls -l  . expand('%:p') . '")'


    exe "nno cd :echo ".string({'one':1, 'two':2})."\r"    ✔
    exe "nno cd :echo ".{'one':1, 'two':2}."\r"            ✘

            Au sein d'une expression, il y a bien coercition automatique de nb en chaîne:

                    exe "nno cd :echo ".42."\r"    ✔

            ... mais pas de dico en chaîne.

            Il faut donc convertir soi-même le dico en chaîne via `string()`.

# For / While

    for [lnum, col] in [[1, 3], [2, 5], [3, 8]]
        echo getline(lnum)[col]
    endfor

            Montre qu'on peut itérer sur une liste de listes (ici [1,3], [2,5] et [3,8]),
            et ainsi modifier la valeur de plusieurs variables simultanément (au lieu d'une seule
            habituellement: for i in list).
            Utile qd on veut itérer sur les clés/valeurs d'un dico.

            La construction de base avec for est:    for var in list
            Cette autre construction:                for [var1, var2, ...] in listlist
            ... est en fait une variante de la 1e, qui n'est possible que lorsque list est composée exclusivement
            de listes ayant toutes la même dimension.


    for [key, value] in items(mydict)
        " do some stuff
    endfor

            Itère sur les clés et valeurs de mydict.


    fu s:grab_words()
        call cursor(1, 1)

        let guard = 0
        let words = []
        let matchline = search('\<\k\+\>', 'cW')

        while matchline && guard < 999
            let words += [matchstr(getline('.'), '\%' . col('.') . 'c\<\k\+\>')]
            let matchline = search('\<\k\+\>', 'W')
        endwhile
        return words
    endfu

            définit la fonction s:grab_words() qui lance une boucle while pour stocker tous les mots
            du buffer courant dans la liste words

                                               NOTE:

            On pourrait aussi utiliser:

                    let words = split(join(getline(1, '$'), "\n"), '\W\+')

            ... qui est encore + rapide.

            En revanche, le principe sur lequel repose cette commande nécessite qu'on puisse facilement
            décrire l'inverse du pattern recherché.
            Facile pour un mot (\W\+), mais plus difficile pour un pattern arbitraire (! foobar = ?).

                                               FIXME:

            Existe-t-il un moyen simple d'inverser un pattern arbitraire (ex: foobar)?
            J'ai tenté:     foobar\zs\_.\{-}\zefoobar\|^\_.\{-}\zefoobar\|\_.*foobar\zs\_.\{-}$

            ... dans:        :echo split(join(getline(1, '$'), "\n"), 'reverse pattern')
            ... ça semble marcher sauf pour le dernier foobar (dernière branche dans le pattern inversé).
            J'ai aussi tenté:

                           :echo split(join(getline(1, '$'), "\n"), '\v((foobar)@!\_.){-1,}')

                                               NOTE:

            Si on sait que le pattern ne peut être présent qu'une fois par ligne, on peut aussi utiliser:

                    :g/pattern/call add(list, matchstr(getline('.'), 'pattern'))

                                               NOTE:

            On peut imaginer que :while teste toujours une condition en fonction de qch qui se situe
            au-dessus d'elle.
            Ex, ici, :while teste si matchline est non nulle. Elle le fait initialement en se basant sur:

                    let matchline = search('\w\+', 'cW')

            ... qui est juste au-dessus.

            Puis, elle le fait en se basant sur:

                    let matchline = search('\w\+', 'W')

            ... qui, certes, se situe après :while au sein de la fonction, mais est bien exécutée AVANT
            le prochain retour vers :while.
            Donc, c'est un peu comme si ce 2e let se situait juste avant :while (JUSTE avant car il n'y
            a rien entre ce :let et :endwhile, et que :endwhile signifie retour vers :while).

                                               NOTE:

            On passe le flag 'c' à search() initialement, car il se peut qu'il y ait un match dès
            le début du buffer.
            Mais ensuite, au sein de la boucle, on ne passe plus ce flag à search(), autrement
            elle trouverait continuellement le même 1er match. Le curseur ne se déplacerait pas,
            on ne trouverait pas les autres matchs, et la boucle while ne se terminerait jamais.

# Let

    let

            affiche l'ensemble des variables actuellement définies


    let list2 = list1

            Affecter à la variable list1 la référence de list2.

            On peut vérifier que list1 et list2 partagent la même référence via:

                    :echo list2 is list1

            Il est probable que pour Vim une donnée soit décomposée en 3 parties (comme dans un fs):

                - son nom (associé à une référence dans une sorte d'annuaire)
                - une référence (pointant vers l'adresse mémoire de la donnée)
                - la donnée elle-même

            Il  ne faut  pas  croire que  dans  la commande  qui  précède, on  a
            dupliqué la donnée stockée dans list1.
            On a simplement créé un nouveau nom pointant vers la référence d'une
            même donnée.
            Ceci explique  pourquoi si on modifie  un item de list1,  on modifie
            par la même occasion list2 ; car les 2 noms d'objets sont associés à
            la même donnée.
            Et réciproquement,  modifier list2  a pour  effet de  modifier aussi
            list1.

            Pour dupliquer la liste stockée dans list1, il faut utiliser la fonction copy() ou deepcopy().


    let [var1, var2; rest] = mylist

            affecter à var1 mylist[0], à var2 mylist[1] et tous les autres items de mylist à la liste rest
            utile pour éviter d'avoir une erreur si la taille de mylist pourrait être plus grand que
            le nb de variables


    let s:myflag = exists('s:myflag') ? !s:myflag : 1
    let s:myflag = !get(s:, 'myflag', 1)

            stocke 1 dans la variable s:myflag si elle vaut 0, 1 autrement

            L'affectation prend en charge le cas où s:myflag n'a pas encore de valeur.
            s:myflag peut être utilisée comme un flag booléen permettant d'exécuter alternativement
            2 actions différentes A, B, A, B... (toggle)

            Utile pex, pour (dés)activer la mise en surbrillance d'un pattern via :match.

                    let s:myflag = ...
                    if s:myflag
                        match /pattern/
                    else
                        match none
                    endif

            Si B n'est pas une action  fixe et dépend d'une valeur, le précédent
            code n'est plus suffisant.
            Dans ce  cas, au lieu  de tester  si s:myflag vaut  0 ou 1,  on peut
            tester si elle  existe ou non et lui affecter  la valeur dont dépend
            B.

            Utile pex,  pour (dés)activer la  mise en surbrillance  d'un pattern
            via matchadd().
            En effet,  cette fois, la  désactivation de la mise  en surbrillance
            n'est  plus  fixe   (:match  none),  mais  dépend   d'un  id  (:call
            matchdelete(id)).

                    if !exists('id')
                        let id = matchadd('SpellBad', 'pattern')
                    else
                        call matchdelete(id)
                        unlet id
                    endif

            L'existence/absence de id répond à la question:    Qu'a-t-on fait la dernière fois, A ou B ?
                                                               Et donc que faire à présent, B ou A ?
            La valeur de id répond à la question:              Comment faire B ?

            Une alternative utilisant le 1er code serait:

                    let s:myflag = exists('s:myflag') ? !s:myflag : 1
                    if s:myflag
                        let id = matchadd('SpellBad', 'pattern')
                    else
                        call matchdelete(id)
                        unlet id    " facultatif
                    endif

            L'inconvénient de cette  2e version est qu'elle crée  2 variables au
            lieu d'une, une pour le flag et une pour l'id.

# Nombres

Vim gère 2 types de nombres, les entiers (signés sur 32 bits, +-2 milliards) et les flottants.

    echo 100            affiche le nombre 100
    echo 0xff           affiche le nb 255 (0x introduit la notation hexadécimale)
    echo 017            affiche le nb 15 (le 1er 0 introduit la notation octale)
    echo 019            affiche le nb 19

                        Au lieu de produire une erreur, Vim ignore silencieusement la notation octale
                        car le chiffre 9 n'existe pas en base 8.
                        De ce fait, il vaut mieux éviter la notation octale quand c'est possible.

    echo 5.45e3         affiche 5450.0 (notation exponentielle)

                        En notation exponentielle, il faut obligatoirement un point et un chiffre après.
                        Ainsi 5e10 n'est pas valide, mais 5.0e10 est valide.

    echo 15.45e-2       affiche 0.1545

    echo 2 * 2.0        affiche 4.0

                        Qd on réalise un calcul ou une comparaison contenant un flottant, Vim convertit
                        les entiers en flottant.

    echo 3 / 2          affiche 1

                        Les deux nb de la division étant des entiers, la division retourne le quotient
                        pour avoir le nb exact, il suffit d'utiliser un flottant qq part (ex: echo 3 / 2.0).

    echo 13 % 5         affiche le reste dans la division de 13 par 5

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


En programmation, on  appelle subroutine (sous-programme/routine/procédure), une
fonction  dont le  code de  sortie ne  nous intéresse  pas, seule  son exécution
compte.
En vimscript, une procédure est appelée via la commande Ex :call.



En cas d'échec,  le code de sortie des  fonctions système est 0, ou -1  si 0 est
une valeur possible de succès.
Pex, en cas d'échec exists() retourne 0 alors que match() retourne -1.
En effet,  0 est une  valeur possible de  succès pour match()  (ex: match('foo',
'f')), mais pas pour exists().

Lorsqu'une fonction utilise -1 comme code de retour pour un échec, on ne peut pas écrire:

        if [!]MyFunc()

... pour réaliser un test. Il faut obligatoirement comparer la sortie à -1:

        if MyFunc() == -1


    :fu Foo

            afficher le code contenu dans la fonction Foo


Parfois, il peut être intéressant d'“éteindre“ temporairement une fonction, c'est à dire l'empêcher
de s'exécuter, sans pour autant la supprimer ou la commenter.
Pour ce faire, il suffit de créer une variable locale avant la définition de la fonction, et de stopper
son exécution si elle vaut 0.
Ex:

            let s:myvar = 1
            fu MyFunc()
                if s:myvar == 0
                    return
                endif
                ...
                main code
                ...
            endfu

On peut aller + loin en ajoutant à la fin du script définissant la fonction 3 commandes pour éteindre
/ allumer / toggle cette dernière:

            com SwitchOnMyFunc     let s:myvar = 1
            com SwitchOffMyFunc    let s:myvar = 0
            com ToggleMyFunc       let s:myvar = !s:myvar

## Arguments

On peut définir une fonction qui attend des arguments identifiés (named arguments) limités à 20,
ainsi que des arguments supplémentaires et optionnels (représenté par '...').


Les arguments optionnels sont utiles pour permettre de modifier la valeur par défaut de certaines variables
utilisées au sein de la fonction. Ex:

    fu MyFunc(...)
        let var1 = a:0 >= 1 ? a:1 : 'foo'
        let var2 = a:0 >= 2 ? a:2 : 'bar'
        let var3 = a:0 >= 3 ? a:3 : 'baz'
    endfu

Pour mieux comprendre, on pourrait tout aussi bien réécrire le code précédent en remplaçant:

    - a:0 >= 1         exists('a:1')
    - a:0 >= 2    →    exists('a:2')
    - a:0 >= 3         exists('a:3')

Une méthode plus élégante consiste à utiliser get() en lui passant en argument entre autres la liste
des arguments optionnels a:000 :

    fu MyFunc(...)
        let var1 = get(a:000, 0, 'foo')
        let var2 = get(a:000, 1, 'bar')
        let var3 = get(a:000, 2, 'baz')
    endfu

Ici MyFunc() attribue par défaut les valeurs 'foo', 'bar' et 'baz' aux variables
var1, var2 et  var3, mais permet de  modifier certaines d'entre elles  si on lui
passe des valeurs en argument (a:1, a:2, a:3).
Toutefois, on ne peut pas modifier n'importe quel sous-ensemble de variables.
Seulement, [var1], [var1, var2] et [var1, var2, var3].
IOW, seulement un sous-ensemble continu qui débute par var1.
Pex on ne pourrait pas modifier:

    - [var1, var3] car il n'est pas continu; il manque var2
    - [var2, var3] car bien que continu il ne commence pas par var1

De ce fait, qd on écrit MyFunc() il faut veiller à affecter a:1 à la variable la
plus susceptible d'être modifiée.
a:2 à la 2e ayant le + de chances d'être modifiée.
a:3 à celle ayant le moins de chances d'être modifiée.
Pk ?
Supposons qu'on  affecte a:3 à  la variable  var1, qui est  celle ayant le  + de
chances d'être modifiée.
À chaque fois qu'on voudra modifier var1,  il faudra passer 3 valeurs à MyFunc()
donc modifier aussi var2 et var3, qui n'en auront peut-être pas besoin.
Auquel cas, il faudra passer à MyFunc() les valeurs par défaut de var2 et var3.


Depuis une fonction on peut accéder en lecture à un argument (a:bar) mais pas en
écriture.
On  ne peut  donc pas  modifier la  valeur d'un  argument, en  revanche on  peut
affecter sa  valeur à une autre  variable qu'on pourra manipuler  comme bon nous
semble.

    :function Foo(bar) ^@ echom a:bar ^@ endfu
    :call Foo("qux")

            définit  la fonction  Foo(), qui  une fois  appelée, echo  la chaîne
            "qux" (bar est le nom du paramètre) qu'on lui passe

    :function Foo(...) ^@ cmd ^@ endfu

            définit la fonction  Foo() qui attend un groupe  d'arguments dont le
            nb est indéterminé (mais limité à 20)

    :function Foo(bar, ...) ^@ cmd ^@ endfu

            définit la fonction Foo() qui attend l'argument bar et un groupe d'arguments

            a:bar    (est évalué à) contenu de l'argument bar
            a:0      nb d'arguments du groupe ... (n'inclut donc pas bar)
            a:1      1er argument du groupe ... (!= bar)

    a:0

            nb d'arguments optionnels  [...] passé à une fonction  (proche de $#
            dans un script bash)

    a:1, a:2

            1er, 2e argument optionnel
            équivaut à a:000[1], a:000[2]; similaire à $1, $2 dans un script bash

    a:000

            liste des  arguments optionnels passés  à la fonction (proche  de $@
            dans un script bash)

    a:{i}

            ième argument; équivaut à a:i

            découvert via :h 41.7 (section: variable number of arguments)

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

    ┌───────────────────────────────┬────────────────────────────────┐
    │ bufexists(42)                 │ le n° est '2                   │
    ├───────────────────────────────┼────────────────────────────────┤
    │ bufexists('foo')              │ le nom est 'foo'               │
    ├───────────────────────────────┼────────────────────────────────┤
    │ bufexists(expand('~/.vimrc')) │ le nom est '/home/user/.vimrc' │
    └───────────────────────────────┴────────────────────────────────┘

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


    if !empty(bufname('%'))

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


    virtcol('.')

            Number of the last screen column occupied by the character under the
            cursor.

                                     NOTE:

            The value of this expression can sometimes be surprising.
            Write this sentence in `/tmp/file`:

                    they would be useful if they were here

            Then, start Vim like this:

                    $ vim -Nu NONE +'norm! 13l' +'lefta 20vs | setl wrap lbr' /tmp/file
                    :echo strcharpart(getline('.'), virtcol('.') - 1, 3)
                    l SPC i~

            You probably expected `SPC u s`.

            Here's what should be displayed:

                                 the cursor should be on this column where a real space resides
                                 v
                    they would be
                    useful if they were
                    here

            From  this position,  `virtcol('.')`  evaluates to  `20`, while  you
            probably expected `14`.
            To better understand what happens, set `'ve'` like this:

                    set ve=all

            And press `g$`, then evaluate `virtcol('.')`; you'll get `20`.
            Maybe  `virtcol('.')` should  evaluate to  `14` when  the cursor  is
            right  before the  space, but  as soon  as you  move the  cursor one
            character forward again  to reach the beginning of  the second line,
            it makes complete sense for `virtcol('.')` to return `21`.

            `virtcol('.')` doesn't  make the difference between  a screen column
            where there is a real character, and one where there is none.
            It includes all of them.

            IOW, if  there is a  column where no  real character resides  in the
            file, between 2 other columns where there *are* real characters, the
            column in the middle is *not* ignored.

            For this reason,  you should prefer `col()` which  is not influenced
            by any option which may change how the text of a file is displayed:

                    - breakat
                    - breakindent
                    - linebreak
                    - showbreak
                    - wrap
                    ...

            Although, I guess it's ok to use  it when you're sure your lines are
            NOT wrapped.

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

    getline(1, '$')

            Retourne toutes les lignes entre la 1e et la dernière du buffer sous la forme d'une liste.
            Chaque item de la liste est une chaîne contenant une ligne du buffer.

            On peut aussi utiliser les fonctions getbufline() et readfile() pour récupérer les lignes
            d'un buffer/ fichier. Chaque fonction est utile dans un contexte différent:

                    - getline()       buffer courant
                    - getbufline()    buffer autre que le courant
                    - readfile()      fichier non chargé dans un buffer

            Pour un buffer déchargé, getbufline() retourne une liste vide [] peu importe son contenu réel.


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


    line2byte(line('$')+1)

            retourne le poids total en octets du buffer courant + 1

            Cette expression est utile pour vérifier qu'un buffer est vide de contenu:

                    if line2byte(line('$')+1) <= 2
                    ...

            Pk `line('$')+1` et pas `line('$')` tout court?
            Parce que `line2byte(line('$'))` retournerait le poids en octets depuis le début du buffer
            jusqu'à la fin de l'avant-dernière ligne, et non pas jusqu'à la fin de la dernière ligne.

            Ainsi, si le buffer contient une seule ligne et qu'elle est non vide, cette expression
            retournera 1.
            Ce `1` signifie sans doute qu'un buffer contient au moins un octet avant tout texte
            (peut-être le BOM = Byte Order Mark ?).
            Et comme `1 <= 2`, le test passera alors qu'il ne devrait pas puisque le buffer est non vide.

            Pk `<= 2`?
            Parce qu'une ligne vide contiendra au moins un 1er caractère (BOM?) et un newline à la fin.


    setline(5, 'hello world!')
    setbufline(2, 5, 'hello world!')

            Remplace la 5e ligne du buffer courant / buffer n° 2 par 'hello world!'.

            Retourne 0 en cas de succès, 1 autrement.

            Ne fait pas bouger  le curseur.  Utile pour substituer une ligne ou  un morceau de ligne
            (y  compris sur  la courante),  via  un mapping  /  commande. Pour ce  faire, donner  à
            setline(), en 2e argument, la sortie de substitute(getline(...), ...).


    setline(5, ['foo', 'bar', 'baz'])

            remplace la 5e ligne du buffer par 'foo', la 6e par 'bar', et la 7e par 'baz'

## Développement de noms de fichiers

Les wildcards suivants sont développés automatiquement dans les noms de fichier (:h wildcard):

    - ?       un caractère

    - *       n'importe quelle chaîne de caractères (le point EXCLU!)

    - **      n'importe quel chemin (le point INCLUS!)
              en l'absence de préfixe, vers un fichier du cwd ou l'un de ses sous-dossiers

    - [abc]   le caractère 'a', 'b' ou 'c'


    echo glob('%:t')        ✘
    echo glob('<cword>')    ✘

    echo expand('%:t')      ✔
    echo expand('<cword>')  ✔

            expand() est la seule à pouvoir développer les expressions '<cword>' et '%:t',
            car glob() ne peut produire que des chemins vers des fichiers EXISTANTS.


Vim développe automatiquement les caractères spéciaux au sein d'une commande :grep, juste avant d'exécuter
cette dernière.  Il les développe même s'ils sont encadrés par des single quotes.
Les quotes sont nécessaires qd on envoit leur développement au shell. Ex:

        :grep -R '<cword>' .

Ici, les single quotes empêchent le shell d'interpréter d'éventuels symboles spéciaux présents
dans le mot sous le curseur avant qu'il n'exécute la commande shell grep.
Mais ce n'est pas suffisant. En effet, si <cword> contient un single quote ce dernier sera mal
interprété par le shell. Il faut donc protéger <cword> avec un outil plus puissant: shellescape().
Exemple:

        :exe 'grep -R '.shellescape(expand('<cword>')) .

Dans ce nouvel exemple, on veut passer <cword> à shellescape() pour que tous ses caractères spéciaux
soient échappés, y compris un single quote.
Si on n'utilise pas expand(), Vim ne développera <cword> qu'au dernier moment, et donc shellescape()
ne recevra pas la chaîne contenant le mot sous le curseur mais la chaîne littérale '<cword>'.
Cette fois, les single quotes autour de <cword> ne servent plus à le protéger du shell
mais à obtenir une chaîne à passer à la fonction expand().

                                               FIXME:

Vim ne développe pas <cword> pour :echo. Normal, elle attend une expression et <cword> n'en est pas une.

Mais pk Vim développe <cword> pour :grep? D'après l'aide :grep attend des [arguments]...

Update:
D'après `:h :grep`:

> Just like ":make", but use 'grepprg' instead of
> 'makeprg' and 'grepformat' instead of 'errorformat'.

Puis, d'après `:h :lmake`:

> Characters '%' and '#' are expanded as usual on a command-line.

Donc, `:make` développe des caractères spéciaux, et `:grep` se comporte comme `:make`.


                                     FIXME:

Avec `:vimgrep`, pk Vim ne développe <cword> que s'il n'est pas quoté?


    expand('$LANG')

            Retourne la valeur de la variable d'environnement $LANG du shell courant.

            Si la session Vim connaît déjà la variable d'environnement, il n'y a pas besoin d'appeler
            expand(): echo $LANG fonctionnera.

            Mais si elle ne la connaît pas, expand() permet de s'assurer qu'elle sera bien développée.
            Pour ce faire, elle lance un shell pour l'occasion.


                                               NOTE:

            expand() et glob() ne sont pas limités à des fichiers, elles peuvent développer:

                    - des caractères spéciaux (:h cmdline-special)
                    - des commandes shell
                    - des globs
                    - des variables d'environnement

            La seule restriction s'impose à glob(), qui rejette toute valeur ne correspondant pas à
            un chemin vers un fichier existant.


    ┌──────────────────┬────────────────────────────────────────────────────────────────────────┐
    │ expand('%')      │ chemin vers le vers fichier courant, relatif au cwd                    │
    ├──────────────────┼────────────────────────────────────────────────────────────────────────┤
    │ ...('%:t')       │ nom du fichier courant (tail of path)                                  │
    ├──────────────────┼────────────────────────────────────────────────────────────────────────┤
    │ ...('<cfile>:t') │ nom du fichier sous le curseur                                         │
    ├──────────────────┼────────────────────────────────────────────────────────────────────────┤
    │ ...('%:p:h')     │ chemin vers le dossier du fichier courant                              │
    ├──────────────────┼────────────────────────────────────────────────────────────────────────┤
    │ ...('%:h:t')     │ chemin vers le dossier parent du fichier courant (la queue de la tête) │
    └──────────────────┴────────────────────────────────────────────────────────────────────────┘


    ┌ développe un éventuel tilde ($HOME) à l'intérieur du précédent développement
    │      ┌ développe <cfile>
    │      │
    expand(expand('<cfile>'))
    glob('<cfile>')

            Retourne le chemin complet vers le fichier sous le curseur.


    expand('<sfile>')

            À l'intérieur d'une fonction, retourne le nom de la fonction, sous la forme:

                function MyFunc
                    ou
                function <SNR>3_MyFunc

            À l'intérieur d'un script (mais à l'extérieur d'une fonction), retourne le chemin vers le script.


                ┌─ respecte 'su' et 'wig'
                │  ┌─ résultat sous forme de liste et non de chaîne
                │  │
    expand('*', 0, 1)
    glob('*', 0, 1, 1)
                    │
                    └─ inclut tous les liens symboliques,
                       même ceux qui pointent sur des fichiers non-existants

            Noms des fichiers / dossiers du cwd.


                                               NOTE:

            Si le dossier de travail est vide, expand() retourne '*', glob() retourne ''.
            glob() est donc plus fiable.
            Ceci est une propriété générale de expand(). Qd elle ne parvient pas à développer qch,
            elle le retourne tq:

                    echo expand('$FOOBAR')
                    $FOOBAR~


    expand('**/README', 0, 1)
    glob('**/README', 0, 1, 1)

            Liste des chemins vers des fichiers README situés dans le cwd ou l'un de ses sous-dossiers.

            À nouveau, si aucun fichier n'est trouvé, expand() retourne ['**/README'],
            tandis que glob() retourne []. glob() est donc plus fiable.


    glob("`find . -name '*.conf' | grep input`", 0, 1, 1)
    expand("`find . -name '*.conf' | grep input`", 0, 1)
    systemlist("find . -name '*.conf' | grep input")

            Sortie de la commande shell:

                    $ find . -name '*.conf' | grep input

            Quelles différences? :

                - glob() ne retourne que des noms de fichier existants.
                  Elle filtre tout ce qui n'est pas exactement un nom de fichier exact.
                  Les messages d'erreurs sont donc supprimés.

                - expand() retourne la sortie brute du shell (erreurs incluses)

                - system() aussi, mais ajoute un newline à la fin, ce qui fait qu'on a une ligne vide
                  en bas du pager


    globpath(&rtp, 'syntax/c.vim', 0, 1, 1)

            Le chemin relatif `syntax/c.vim` est ajouté en suffixe à chaque chemin absolu du 'rtp'.
            Si le résultat correspond à un fichier existant, il est ajouté à une liste.
            `globpath()` retourne la liste finale, une fois que tous les chemins du 'rtp' ont été utilisés.


    globpath(&rtp, '**/README.txt', 0, 1, 1)

            Idem, sauf que cette fois, le suffixe contient un wildcard, qui à chaque fois est développé
            en une liste de 0, 1 ou plusieurs fichiers correspondant.


                                               NOTE:

            Plus généralement, globpath() attend 2 arguments, tous 2 des expressions évaluées en chaînes:

                    - la 1e doit stocker des chemins séparés par des virgules
                    - la 2e un chemin relatif vers un fichier, incluant éventuellement des wildcards


    substitute(glob2regpat(&wig), ',', '\\|', 'g')

        \.bak\|.*\.swo\|.*\.swp\|.*\~\|.*\.mp3\|.*\.png,...~

            `glob2repat()` convertit un pattern de fichier en un pattern de recherche.
            Utile qd on cherche un nom de fichier, dont le nom est écrit dans un buffer,
            et qui est décrit par un glob contenu dans une option tq 'wig'.

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

                    - col('.') - len(matchstr(getline('.')[:col('.')-2], '\S\+'))

                            remplace le texte devant le curseur;
                            le texte étant défini comme une séquence de non-whitespace

            Bien sûr, la fonction CustomMenu() pourrait utiliser/construire n'importe quelle liste
            contenant les items qu'on souhaite pouvoir insérer automatiquement.
            Pex, la liste des contenus des registres.

            Toutefois, si ceux-ci contiennent des LF, le menu les traduit en NUL.
            Peut-être car `complete()` n'est pas censée accueillir des items multi-lignes.

            On notera également l'instruction return '' qui est nécessaire pour éviter que `CustomMenu()`
            ne retourne le code de sortie 0 qui serait alors automatiquement inséré à la suite du 1er
            item (foo0), sans que le menu ne s'affiche.


    if [!]empty(expr)

            teste si expr est vide en retournant le nombre 1 si expr est vide, 0 autrement (! inverse le test)

            expr peut être une chaîne, une liste, un dictionnaire ou un nb (vide = 0)


    if exists('*myfunc')
    if exists(':cmd')
    if exists('#current_word#CursorHold')

            Teste l'existence de:

                - d'une fonction du nom de `myfunc`

                - de la commande Ex `:cmd`

                - d'une autocmd dans l'augroup `current_word` surveillant l'évènement `CursorHold`


    if has('gui_running')

            teste si Vim tourne en gui

            la liste des fonctionnalités supportées par Vim est lisible via: :h feature-list


    confirm('Are you sure?', "&yes\n&no\n&quit", 2)

            Affiche une ligne affichant le message 'Are you sure?', propose à l'utilisateur
            un choix entre 'yes', 'no' et 'quit', attend  que l'utilisateur tape 'y', 'n' ou 'q'
            et retourne le n° du choix.
            Le choix par défaut, si on appuie seulement sur Enter, est 'no' (3e argument: 2).

            Les choix doivent être séparés par des \n.
            Pour un choix donné, on peut choisir quelle lettre permet de le sélectionner en la faisant
            précéder de &.
            Retourne 0 si l'utilisateur appuie sur C-c ou Esc.


    let password = inputsecret('Enter sudo password:') . "\n"
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


    mapcheck('<C-G>', 'c')

            retourne le {rhs} du mapping dont le {lhs} est C-g

    setcmdpos(6)

            positionne le curseur juste avant le 6e octet sur la ligne de commande

            Si aucun des 5 premiers caractères de la ligne de commande n'est multi-octets,
            positionne le curseur juste avant le 6e caractère.

            Ne fonctionne que lorsqu'on édite la ligne de commande:

                    - en y insérant l'évaluation d'une expression via C-r
                    - en la remplaçant entièrement par l'évaluation d'une expression via C-\ e

            Je n'ai pas réussi à l'utiliser directement au sein du (pseudo?) registre expression
            dans lequel on entre qd on tape C-r ou C-\ e.
            En revanche, elle fonctionne correctement qd on évalue une fonction custom juste après.

            Qd on évalue une fonction custom:

                - via C-\ e, setcmdpos() permet de positionner le curseur sur la nouvelle ligne de
                  commande, l'ancienne étant remplacée par l'évaluation

                - via  C-r, setcmdpos()  permet  de positionner  le curseur  sur  l'ancienne ligne  de
                  commande (qui n'est  pas remplacée), avant que l'évaluation ne soit insérée là où se
                  trouve le curseur

            Qd on utilise  C-\ e ou C-r = pour  évaluer une fonction custom, il ne  sert à rien de
            demander  à cette  dernière de  retourner des  caractères de  contrôle tq  <cr> pour
            exécuter la ligne de commande ou <Left>, <Right> pour déplacer le curseur.

            En effet, C-\ e  et C-r ne peuvent qu'insérer des caractères,  donc des caractères de
            contrôle seraient insérés littéralement et non interprétés comme des commandes.

            Si on  veut déplacer le  curseur sur  la ligne de  commande après que  les caractères
            retournés par la fonction custom aient été insérés, il faut utiliser soit:

                    - setcmdpos() au sein de la fonction custom

                    - des <left>, <right> après que la fonction custom ait été évaluée; pex au sein d'un mapping:

                            cno <f8> <c-\>e MyFunc()<cr><left><left>

            On ne rencontrerait pas ce pb avec  un mapping auquel on passerait l'argument <expr>, et
            auquel on demanderait de taper les touches retournées par une fonction custom.

            Dans  ce cas,  les touches  de contrôle  ne  seraient pas  insérées sur  la ligne  de
            commande, mais interprétées comme des actions (validation, mouvement).

                                               NOTE:

            La position du curseur via `setcmdpos()` n'est pas établie au même moment selon qu'on
            utilise `C-r =`  ou  `C-\ e` / `C-r C-r =`:

                    - C-r =        après avoir évalué l'expression, MAIS AVANT de l'insérer

                    - C-r C-r =    après avoir évalué l'expression
                      C-\ e


    submatch()

            À l'intérieur d'une expression de remplacement, permet d'accéder à tout ou partie texte
            matché par le pattern.

            submatch(0) = tout le texte
            submatch(1) = 1ère sous-expression capturée

            On peut utiliser une expression de remplacement (et donc submatch()) dans une commande de substitution:

                    :s:pattern:\=expression:

            ou dans la fonction substitute():

                    substitute('text', 'pattern', '\=expr', 'flags')


                                               NOTE:

            Si on utilise des double quotes pour '\=expr', bien penser à doubler les backslashs
            à l'intérieur y compris le 1er: "\\=expr"


                                               NOTE:

            Alternativement, on peut remplacer '\=expr' par une expression lambda :

                    substitute('text', 'pattern', {-> expr}, 'flags')


    system('cmd')
    system('cmd', 'input')

            retourne la sortie de la commande shell cmd (en écrivant 'input' sur son entrée standard)

    system('ls -l '.expand('%:p'))

            retourne un listing détaillé (ls -l) du fichier courant

            Cette commande illustre le fait que Vim peut évaluer une concaténation de chaînes avant
            d'en passer le résultat à une fonction acceptant une expression comme argument.
            En effet, une concaténation d'expressions est une expression.


    system('tmux send-keys -t 1.2 "echo hello" Enter')

            exécute la commande shell `$ echo hello` dans le 2e pane de la 1e fenêtre de la session
            tmux courante


    tabpagenr()
    tabpagenr('$')

            retourne le n° de l'onglet courant; du dernier onglet


    exe (tabpagenr()-1).'tabnew'

            ouvre un nouvel onglet juste avant l'onglet courant


    taglist('pattern')

            Retourne la liste des tags matchant pattern.

            Chaque item de la liste est un dictionnaire, contenant entre autres les clés `name` et `filename`.


    taglist('pattern')[0].name
    taglist('pattern')[0].filename
    map(taglist('pattern'), 'v:val.name')

            retourne le nom:

                    - du 1er tag                         matchant pattern
                    - du fichier contenant le 1er tag    "
                    - des noms de tous les tags          "

    visualmode()

            retourne le type de la dernière sélection visuelle dans le buffer courant ('v', 'V', '^V')

            Utile pour passer en argument le type de la dernière sélection à une fonction souhaitant
            agir sur cette dernière.
            Par exemple , si visualmode() retourne 'v' la fonction utilisera les marques `< et `>,
            et si elle retourne 'V' la fonction utilisera les marques '< et '>.

## Expression lambda / closure

Document that  when you define  a lambda which refers  to some variables  in the
rhs, absent  from the  lhs, they should  all be assigned  before the  lambda (at
least one).

MWE:

        fu Func()
            let l:Test = { -> foo + bar ==# 3 }
            let foo  = 1
            let bar  = 2
            return l:Test()
        endfu
        echo Func()
        E121~

        fu Func()
            let foo  = 1
            let l:Test = { -> foo + bar ==# 3 }
            let bar  = 2
            return l:Test()
        endfu
        echo Func()
        1~

Explanation: <https://github.com/vim/vim/issues/2643#issuecomment-366954582>

---

The name of a variable storing a  lambda or funcref must begin with an uppercase
character, because  you could  drop the  `l:`, in  which case  there could  be a
conflict with a builtin function (e.g. you've used the variable name `len`).
The name **must** start with an uppercase character.

But now that your variable starts with  an uppercase character, there could be a
conflict with a global custom function.
So, the name **should** be scoped with `l:` to avoid E705.
From `:h e705`:

> You cannot have both a Funcref variable and a function with the same name.

Indeed, without `l:`, if you run this inside a function:

    let Lambda = {-> 123}
    echo Lambda()

and you have  a global custom function  named `Lambda`, Vim will  not know which
definition to use.

Review this section, and add `l:` whenever it makes sense.

---

    {args -> expr}

Il  s'agit d'une  expression lambda,  qui crée  une nouvelle  fonction numérotée
retournant l'évaluation d'une expression.
Elle diffère d'une fonction régulière de 2 façons:

   - Le corps de l'expression lambda est une expression et non une séquence de
     commandes Ex.

   - Les arguments ne sont pas dans le scope `a:`.

---

    let F = {arg1, arg2 -> arg1 + arg2}
    echo F(1,2)
    3~

---

    fu A()
        return 'i am A'
    endfu
    fu B()
        let A = {-> 42}
        return A()
    endfu
    echo B()
    E705: Variable name conflicts with existing function: A~

    fu A()
        return 'i am A'
    endfu
    fu B()
        let l:A = { -> 42 }
        return l:A()
    endfu
    echo B()
    42~

Qd  on  se trouve  à  l'intérieur  d'une fonction,  et  qu'on  doit stocker  une
expression  lambda, ou  une funcref,  dans une  variable, il  faut toujours  lui
donner le scope `l:`.
En effet, le nom doit commencer par  une majuscule, ce qui pourrait provoquer un
conflit entre avec une fonction publique de même nom.

---

    let F = { -> 'hello'.42 }
    echo F()
    hello42~

Une expression lambda peut ne pas avoir d'arguments.

---

    {'<lambda>42'}

Le nom de la fonction numérotée créée par une expression lambda suit ce schéma.
En cas d'erreur au sein de cette dernière, on pourra donc exécuter:

    fu {'<lambda>42'}

... pour lire son code:

                    let F = {-> 'hello'.[42]}
                    echo F()
                    E15: Invalid expression: <lambda>15    ✘~

---

    echo map([1, 2, 3], {_,v -> v + 1})
    [2, 3, 4]~

    echo sort([3,7,2,1,4], {a,b -> a - b})
    [1, 2, 3, 4, 7]~

On peut,  entre autres,  utiliser des  expressions lambda  comme 2e  argument de
`filter()`, `map()` et `sort()`.

---

    let timer = timer_start(500, {-> execute("echo 'Handler called'", '')}, {'repeat': 3})
    Handler called~
    Handler called~
    Handler called~

Les expressions lambda sont aussi utiles pour des timers, canaux, jobs.

---

Si un timer est  exécuté au moment où on se trouve sur  la ligne de commande, le
curseur peut temporairement quitter cette dernière et s'afficher dans le buffer.

    nno <expr> cd Func()
    fu Func()
        let my_timer = timer_start(2000, { -> execute('sleep 1', '') })
        return ''
    endfu

Taper `cd`, puis écrire qch sur la ligne de commande et attendre.

---

    ✘
    call timer_start(0, {-> execute('call FuncA() | call FuncB()')})
    ✔
    call timer_start(0, {-> FuncA() + FuncB()})

    ✘
    call timer_start(0, {-> execute('if expr | call Func() | endif')})
    ✔
    call timer_start(0, {-> expr ? Func() : 0})
    ✔✔
    call timer_start(0, {-> expr && Func()})

    ✘
    call timer_start(0, {-> execute('if expr | call FuncA() | endif | call FuncB()})
    ✔
    call timer_start(0, {-> (expr ? FuncA() : 0) + FuncB()})
    ✔✔
    call timer_start(0, {-> (expr && FuncA()) + FuncB()})

On  n'a  pratiquement  jamais  besoin d'utiliser  `execute()`  et  `:call`  pour
exécuter une fonction via un lambda.

`:call` est nécessaire sur la ligne de  commande car Vim s'attend à exécuter une
commande.
`:call` n'est pas toujours nécessaire dans un lambda, car Vim s'attend à évaluer
une expression, et une fonction EST un type d'expression.

---

Qd  on exécute  une fonction  via  un lambda,  sa  valeur de  sortie n'a  aucune
importance.

---

N'utilise `||` et `&&` comme connecteur  logique que lorsque c'est nécessaire et
qu'ils correspondent réellement à ce que tu veux faire.
Autrement, préfère un opérateur plus simple tq `+`:

                           exécute 2 fonctions
    ┌────────────────────┬─────────────────────────────────────────┐
    │ FuncA() && FuncB() │ à condition que la 1e ait réussi        │
    ├────────────────────┼─────────────────────────────────────────┤
    │ FuncA() || FuncB() │ à condition que la 1e ait échoué        │
    ├────────────────────┼─────────────────────────────────────────┤
    │ FuncA() + FuncB()  │ peu importe que la 1e ait réussi ou non │
    └────────────────────┴─────────────────────────────────────────┘

---

        expr && FuncA() + FuncB()
    ⇔
        exécute `FuncA` ET `FuncB` à condition que `expr` soit vraie


        (expr && FuncA()) + FuncB()
    ⇔
        exécute `FuncA` à condition que `expr` soit vraie, PUIS `FuncB`


Cette différence découle du fait que l'opérateur `+` a priorité sur `&&`.

Confirmation via:

    echo 0 && 1 + 1
    0~

    echo (0 && 1) + 1
    1~

---

    echo map(range(65, 90), {x -> nr2char(x)})
    [ 'A', 'B', ... ]          attendu~
    [ '', '^A', '^B', ... ]    obtenu~

Pk n'obtient-on pas la liste des lettres majuscules ?
Car  qd  le 2e  argument  de  `map()` est  une  funcref,  `map()` lui  envoit  2
arguments:

   1. l'index (pour une liste) ou la clé (pour un dico) de l'item courant
   2. la valeur de l'item courant

`map()` utilise ensuite la fonction associée  à la funcref pour remplacer chaque
item de la liste.

Donc, dans l'exemple précédent, pour remplacer les nbs 65 à 90, `map()` envoit à
`nr2char()` les valeurs suivantes:

   - nr2char(0, 65)
   - nr2char(1, 66)
     ...
   - nr2char(25, 90)

Or, pour `nr2char()`, le 2e argument est un simple flag:

   - 0 signifie qu'on veut utiliser l'encodage courant

   - 1 l'encodage utf-8

`65` ... `90` sont interprétés comme un `1`.

De plus, `nr2char()` ne reçoit pas les bons codepoints:

    65 ... 90  ✔ ce qu'ell devrait recevoir
    0  ... 25  ✘ ce qu'elle reçoit

Solution:

    map(range(65,90), {_,v -> nr2char(v)})
                       ^^

Conclusion:

Pour pouvoir se  référer à un argument  reçu par une expression  lambda, il faut
correctement tous les déclarer.
Donc,  qd une  fonction  accepte  une expression  lambda  en argument,  toujours
regarder quels arguments elle envoit à cette dernière.
Ici, `map()` n'en envoit pas 1 (`x`), mais 2 (`_`, `v`).


    fu Foo(arg)
        let i = 3
        return {x -> x + i - a:arg}
    endfu
    let Bar = Foo(4)
    echo Bar(6)
    5~

L'expression lambda utilise dans son calcul les variables `i` et `a:arg`.

`i` appartient  à la portée  locale à `Foo()`,  tandis que `a:arg`  appartient à
celle des arguments de `Foo()`.
L'expression lambda ne se plaint pas que les variables ne sont pas définies :

    E121: Undefined variable: i~
    E121: Undefined variable: a:arg~

... car elle  a la particularité de  pouvoir accéder aux variables  de la portée
extérieur; on parle de “closure“ (clôture).


    fu Foo()
        let x = 0
        fu! Bar() closure
            let x += 1 " pas d'erreur, grâce à `closure`
            return x
        endfu
        return funcref('Bar')
    endfu

    let F = Foo()
    echo F()
    1~
    echo F()
    2~
    echo F()
    3~

L'incrémentation  de `x` au sein de `Bar()` ne soulève pas d'erreur:

    E121: Undefined variable: x~

...  car  `Bar()`  porte  l'attribut  `closure` qui  lui  permet  d'accéder  aux
variables de la portée extérieure (`Foo()`).

La sortie de `F()` est incrémentée à chaque appel.
Ceci prouve  qu'une fonction  portant l'attribut `closure`  peut continuer  à se
référer à la portée d'une fonction  extérieur même après qu'elle ait terminé son
exécution.

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


    if !empty(win_findbuf(42))

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


    winnr()    winnr('#')    winnr('$')

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


    @=winnr('#') CR C-w c      mode normal
    :exe winnr('#').'close'    mode Ex

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


    escape(file, ' \')

            échappe les espaces et les backslash dans le nom de fichier file
            plus généralement tous les caractères présents dans le 2e argument de escape() sont échappés


    if filereadable('/path/fo/file')

            teste si /path/to/file PEUT ÊTRE LU (et donc aussi son existence)

            Ce test peut s'écrire simplement comme ça car le code de retour de filereadable()
            en cas d'échec est 0. Si c'était -1, il faudrait obligatoirement comparer la sortie à -1.


    if !empty(glob('/path/to/file'))

            TESTE L'EXISTENCE de /path/to/file (fonctionne même si on n'a pas les droits pour le lire)

            Ce test peut s'écrire simplement comme ça car le code de retour de empty()
            en cas d'échec est 0. Si c'était -1, il faudrait obligatoirement comparer la sortie à -1.

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


    :exe 'e '.fnameescape('fname')

            Exécute la commande  Ex ':edit fname' en ayant  échappé les symboles
            spéciaux que fname contient.
            Si  fname contient  un %  ou un  |, ça  permet d'éviter  que Vim  ne
            développe ces symboles.


    !isdirectory(expand('$HOME') . '/dir')

            teste la non-existence du dossier /home/user/dir

            Ce test peut s'écrire simplement comme ça car le code de retour de isdirectory()
            en cas d'échec est 0. Si c'était -1, il faudrait obligatoirement comparer la sortie à -1.


    mkdir(expand('$HOME').'foo/bar', 'p')

            crée le dossier /home/user/foo/bar, en créant les dossiers intermédiaires si nécessaire
            (2e argument 'p')


    readfile('/tmp/foo')
    readfile(fname, '', 10)
    readfile(fname, '', -10)

            Retourne une liste dont les items sont des lignes du fichier `/tmp/foo`:

                    - toutes
                    - les 10 premières
                    - les 10 dernières


    let words = split(join(readfile('/tmp/foo'), "\n"), '\W\+')

            stocke dans la variable words une liste contenant le 1er mot de chaque ligne du fichier /tmp/foo

            Ceci illustre comment on peut utiliser la fonction split() pour récupérer toutes les occurrences
            d'un pattern. Ne fonctionne que si on peut facilement décrire l'inverse du pattern.
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

                    exe '!shell_cmd ' . shellescape('#' . l:mycolor, 1)


    :let @" = 'foo;ls'     | exe 'grep! '.shellescape(@",1).' .'
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


    system('chmod +x -- ' . shellescape(expand('%')))

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

            Retourne / capture le nom d'un fichier temporaire. Ex:

                    /tmp/abcd123/0

            Le dossier le contenant est automatiquement créé dans les 2 cas.


                                               NOTE:

            Le simple fait d'invoquer la commande shell `mktemp` provoque également la création d'un
            dossier temporaire par Vim:

                    echo expand('`mktemp -d /tmp/.pgm.XXXXXXXXXX`')
                    /tmp/abcd123/ + /tmp/.pgm.abcdef12345~
                    call system('mktemp -d /tmp/.pgm.XXXXXXXXXX')
                    /tmp/abcd123/ + /tmp/.pgm.abcdef12345~

            Toutefois, on préfèrera utiliser `tempname()`, car qd on le réinvoquera, Vim créera tous
            les fichiers suivants dans le même dossier.
            De plus, qd on quittera Vim, il supprimera automatiquement le dossier.


    writefile(['foo', 'bar'], 'file', 'a')

            ajoute à la fin du fichier file les chaînes 'foo' et 'bar', séparé par un newline
            le 3e argument 'a' est un flag qui indique à la fonction d'ajouter (append) les chaînes
            au fichier sans écraser son contenu

## Historique

    histadd('/', strftime('%c'))

            ajouter dans l'historique de recherche la date du jour

                                               NOTE:

            Il existe d'autres historiques qu'on peut manipuler via histadd(), histdel(), histget() et histnr():

                : ou cmd       ligne de commande
                / ou search    recherche
                = ou expr      registre expression
                @ ou input     dernières valeurs fournies à la fonction input()
                > ou debug     commandes de déboguage

    histdel('/')    histdel('/', -1)    histdel('/', '^a.*b$')

            supprimer de l'historique de recherche:

                    - toutes les entrées
                    - la dernière entrée
                    - toutes les entrées commençant par a et finissant par b

    histget('/', 5)    histget('/')

            retourne la 5e entrée de l'historique de recherche; la dernière entrée

                                               NOTE:

            - on peut fournir un n° d'index absolu (nb positif), ou relatif par rapport à la fin
              (nb négatif, -1 = dernière entrée)

            - l'index absolu d'une entrée dans l'historique de recherche ne correspond pas forcément
              au n° de la ligne sur laquelle il est présent dans la fenêtre qui pop via q/

    histnr('/')

            retourne le n° d'index de la dernière entrée dans l'historique de recherche


    :search something | call histdel('/', -1) | let @/ = histget('/')

            supprime la dernière recherche, et restocke dans le registre recherche l'avant-dernière
            utile après une recherche dont on ne souhaite laisser aucune trace (ou alors utiliser :keeppatterns)

## Mappings

    if empty(maparg('-', 'n'))

            teste si la touche - est map à quelque chose en mode normal


    maparg('<C-L>', 'v')

            retourne le {rhs} du mapping v_ctrl-l

            Qd le 2e argument est une chaine vide, maparg() cherche un {rhs} pour le mode normal,
            visuel et operator-pending.
            S'il existe 2 mappings utilisant C-l comme {lhs}, un global et un buffer-local, c'est le {rhs}
            du buffer-local qui est retourné. Même chose qd on demande un dictionnaire (maparg(..., 0, 1)).


    maparg('<C-L>', 'v', 0, 1)

            retourne un dictionnaire contenant toutes les infos concernant le mapping v_ctrl-l
            Entre autres:

              est-il silencieux?
              est-il local au buffer?
              son lhs, son rhs
              le rhs est-il récursif?
              son rhs est-il le résultat d'une expression?
              attend-il avant d'exécuter le {rhs} si un autre mapping existe qui commence par le même {lhs}?
              son mode
              le sid du fichier dans lequel il a été défini (3 = vimrc)

              Qd le 3e argument de maparg() est non nul, le 1er argument n'est plus interprété comme le
              {lhs} d'un mapping mais le {lhs} d'une abréviation.


    exe 'nnoremap <Tab> ==' . maparg('<Tab>', 'n')

            préfixe '==' au {rhs} de <Tab> en mode normal

            Pex, si <Tab> en mode normal était associé à 'gm', après la commande précédente,
            il est associé à '==gm'


    mapcheck('abc', 'n')

            Retourne le rhs d'un mapping en mode normal si:

                    'abc' est le début de son lhs (lhs =~ ^abc)
                    ou inversement si le lhs d'un mapping est le début de 'abc' (abc =~ ^lhs)

            Si 'abc'  est le  début du  lhs d'un mapping  (ex: 'abcd'),  alors définir  un nouveau
            mapping dont le lhs  est 'abc' posera pb car lorsqu'on appuiera  sur 'abc', Vim attendra
            3s (&timeoutlen) avant d'exécuter le rhs.

            Réciproquement, si le lhs d'un mapping débute de la même façon que 'abc' (ex: 'ab'),
            alors  définir un  nouveau mapping  dont le  lhs est  'abc' posera  là encore  pb, car
            lorsqu'on appuiera sur 'ab', Vim attendra 3s avant d'exécuter son rhs.

            En testant  que la sortie de  mapcheck('abc') est bien  vide, on peut s'assurer  dans un
            script qu'on peut définir un nouveau mapping dont le {lhs} est 'abc' sans qu'il n'y ait
            jamais d'ambiguïté (pour 'abc' ou pour un autre qui commence pareil: 'a', 'ab').


    hasmapto('abc', 'n')

            Retourne 1 s'il existe un mapping en mode normal, dont le rhs contient `abc`.
            0 autrement.

            Utile dans un plugin pour vérifier si l'utilisateur a déjà associé une séquence de touches
            à un `<plug>` mapping.

## Recherche / curseur

    cursor(5,10)

            positionne le curseur sur la 10e colonne de la 5e ligne du buffer
            retourne 0 si le curseur a pu être positionné, -1 autrement

            si le n° de ligne est nul le curseur ne change pas de ligne (idem pour la colonne)
            si le n° de ligne est supérieur au nb de lignes du buffer, le curseur se déplace sur la dernière (idem pour la colonne)

            Utile pour positionner le curseur avant de débuter une recherche avec search().

    getcurpos()

            Retourne une liste de 5 nb correspondant aux coordonnées du curseur.

            Le retour est généralement sauvegardé  dans un variable pour pouvoir
            restaurer la position du curseur plus tard.  Ex:

                    let save_cursor = getcurpos()


                                     NOTE:

            Ne  jamais utiliser  `getpos()` pour  sauvegarder puis  restaurer la
            position du curseur. `getpos()` ne sauvegarde pas l'attribut 'curswant'.

            https://vi.stackexchange.com/a/15566/16670


    search(pattern, [flags, stopline])

            Cherche pattern à partir du curseur.
            Retourne le n° de ligne du match s'il y en a un, 0 autrement.

            Le curseur se déplace jusqu'au match.
            stopline est un n° de ligne au-delà duquel la recherche doit s'arrêter.
            On peut passer des flags modifiant le comportement de search(), entre autres:

            ┌─────┬─────────────────────────────────────────────────────────────────────────────┐
            │ 'b' │ recherche vers l'arrière                                                    │
            ├─────┼─────────────────────────────────────────────────────────────────────────────┤
            │ 'c' │ accepte un match à l'endroit où se trouve le curseur                        │
            │     │ le curseur ne se déplace pas                                                │
            ├─────┼─────────────────────────────────────────────────────────────────────────────┤
            │ 'e' │ déplace le curseur à la fin du match (au lieu du début)                     │
            ├─────┼─────────────────────────────────────────────────────────────────────────────┤
            │ 'n' │ ne déplace pas le curseur                                                   │
            ├─────┼─────────────────────────────────────────────────────────────────────────────┤
            │ 's' │ pose la marque ' à l'endroit où se trouve le curseur avant la recherche     │
            ├─────┼─────────────────────────────────────────────────────────────────────────────┤
            │ 'w' │ wrap / boucle à la fin du fichier                                           │
            ├─────┼─────────────────────────────────────────────────────────────────────────────┤
            │ 'W' │ ne wrap pas à la fin du fichier                                             │
            ├─────┼─────────────────────────────────────────────────────────────────────────────┤
            │ 'z' │ cherche à partir du curseur et non de la colonne 0                          │
            │     │ Même si on omet 'z', et que la recherche commence à partir de la colonne 0, │
            │     │ search() skip les matchs précédant le curseur.                              │
            └─────┴─────────────────────────────────────────────────────────────────────────────┘

                                     NOTE:

            Always use the `W` flag when you use `search()` in a while loop.
            Otherwise, you may end up in an infinite loop.

                                     NOTE:

            What's the use of 'z'?
            It seems that if we omit it, Vim does the same thing:

>                   When the 'z' flag is not given, searching always starts in
>                   column zero **and then matches before the cursor are skipped**.

            If  the matches  before  the  cursor are  skipped,  then why  bother
            searching from column zero?

           Answer: The purpose of 'z' is probably to increase performance.
           Even if searching from column 0, then ignoring the matches before the
           cursor, gives the same result as  searching from the cursor, it costs
           more time.


                                     NOTE:

            Une commande Ex exécutée depuis le mode visuel nous fait toujours quitter ce dernier.
            On ne peut donc pas directement invoquer `search()` pour étendre la sélection jusqu'à
            la prochaine occurrence d'un pattern arbitraire:

                call search('pat')                     ✘ cherche `pat` depuis le mode normal

                                                         Pk le mode normal?
                                                         Car après après avoir appuyé sur Enter pour
                                                         exécuter une commande Ex, on est immédiatement
                                                         en mode normal.

                call search('pat') | norm! gv          ✘ cherche `pat` depuis le mode normal
                                                         et restaure la dernière sélection visuelle

                call search('pat') | norm! m'gv``      ✔

                exe 'norm! gv' | call search('pat')    ✔ cherche `pat` depuis le mode visuel (*)
                                                         et ce faisant met à jour la sélection

            (*) Cette fois, 'norm! gv' restaure la sélection visuelle avant d'invoquer `search()`.


    getline(search('foo', 'bcnW'))

            retourne le contenu de la précédente ligne où se trouve le pattern 'foo' sans faire
            bouger le curseur

    search('(', 'b', line("w0"))

            cherche vers l'arrière le caractère '(' en s'arrêtant à la 1e ligne de la fenêtre
            retourne le n° de ligne du match

    search('END', '', line("w$"))

            cherche la chaîne 'END' en s'arrêtant à la dernière ligne actuellement visible dans la fenêtre
            retourne le n° de ligne du match

    search('\v<' . nr2char(getchar()), 'W', line('.'))

            demande une frappe au clavier, et déplace le curseur sur le prochain mot commençant
            par la lettre tapée

            line('.') indique à Vim d'arrêter sa recherche au-delà de la ligne courante (stopline)

                                               NOTE:

            search() retourne le n° de ligne d'un match, mais il déplace aussi le curseur.
            Ici, c'est le déplacement qui nous intéresse (pas le code de retour).

    searchpos()

            similaire à search() à ceci près qu'elle retourne une liste [lnum, cnum]

    setpos('.', save_cursor)

            restaure la position du curseur sauvegardée dans la variable save_cursor via la fonction getcurpos()

            le 1er argument de setpos() détermine de quel objet la fonction va définir la position:
            le curseur = . ou une marque = 'x

