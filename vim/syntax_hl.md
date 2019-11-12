# ?

    :syn-keepend

By default,  a contained match can  consume a match  for the end pattern  of the
outer region.
This forces the  outer region to look  further for a match for  its end pattern,
which extends the text it highlights.

This is useful for nesting.
For example, a block that starts with `{` and ends with `}`, can contain another
similar block.
An encountered `}` will then end the contained block, but not the outer block.

If you don't want this, the `keepend`  argument will make the matching of an end
pattern of the outer region also end any contained item.
This makes it impossible to nest the same region, but allows for contained items
to highlight parts  of the end pattern,  without causing that to  skip the match
with the end pattern.

Example:

    :syn match  vimComment /"[^"]\+$/
    :syn region vimCommand start=/set/ end=/$/ contains=vimComment keepend

The `keepend`  makes the `vimCommand`  always end at the  end of the  line, even
though the contained `vimComment` includes a match with the `<EOL>`.

When `keepend` is  not used, a match  with an end pattern is  retried after each
contained match.
When `keepend` is  included, the first encountered match with  an end pattern is
used, truncating any contained matches.

##
##
##
# How to rank the 3 subcommands `keyword`, `match`, `region`, performance-wise?

From the most performant to the least one:

   1. keyword
   2. match
   3. region

This order seems to be suggested in [this comment][1].

`match` is slower because Vim must  search for a regex.

`region` is probably slower because Vim must search for 2 regexes.
Besides, a region is more complex (`skip`, `keepend`, ...).

##
# Syntax groups/clusters
## What can a syntax group contain?

Other syntax groups.

## What can a syntax cluster contain?

Syntax groups and other clusters.

###
## Are syntax groups local to a buffer?

Yes.

    :sp /tmp/lua1.lua
    :e /tmp/lua2.lua
    :syn list luaOperator
        luaOperator    xxx and or not~
                           links to Operator~

    :syn match luaOperator /abc/
    :syn list luaOperator
        luaOperator    xxx and or not~
                           match /abc/~
                           links to Operator~

    :e#
    :syn list luaOperator
        luaOperator    xxx contained not and or~
                           links to Operator~

The new `match` item is *not* in the `luaOperator` syntax group of `lua1.lua`.
This is because a syntax group is local to the buffer where it was defined.

## Are clusters local to a buffer?

Yes.

    " in a markdown buffer
    :syn list @Spell
    Spell          cluster=NONE~

    " in a help buffer
    :syn list @Spell
    E392: No such syntax cluster: @Spell~

##
## Is the name of a syntax group case-sensitive?

No.

    :sil! syn clear xfoo xFOO
    :syn match xfoo /lowercase/
    :syn match xFOO /uppercase/
    :syn list xfoo
    xfoo           xxx match /lowercase/ ~
                       match /uppercase/ ~

If Vim considered `xfoo` as a different  group than `xFOO`, it would not contain
the second match.

###
## How to clear all syntax groups in the current buffer?

    :syn clear

###
## Why are there lua, python, ruby, ... syntax groups in a Vim buffer?

The default  Vim syntax plugin  includes many other  syntax plugins in  case the
user embeds another scripting language in its Vimscript.
Indeed, you can script Vim with lua, python, ruby, ...

## I've just installed a syntax item by executing a `:syn` command.  After reloading the buffer, it's lost!  Why?

When you reload a buffer, Vim sources:

    $VIMRUNTIME/syntax/nosyntax.vim

which removes all syntax items.

After that, it re-sources the syntax plugins.
If your custom item is not defined in one of them, it won't be re-installed.

##
# Getting information
## How to get the name of the syntax plugin used to highlight the current buffer?

    echo b:current_syntax

### Why shouldn't I use `&syntax`?

It's unreliable.

`&syntax` copies the value of `&ft` when `FileType` is fired.
But after that, the syntax groups may be removed, and other syntax groups may be
sourced.

###
## How to get all the syntax items defined in the current buffer?

    :sy

## How to get the list of all items inside `xGroup`?  Inside `@xCluster`?

    :syn list xGroup

    :syn list @xCluster

###
## `:syn list xFoo` outputs `xFoo xxx links to Bar`.  There's no item!  What does it mean?

Vim  has added  the HG  `Bar` from  a syntax  plugin sourced  for a  buffer (not
necessarily the current one).
And this HG exists no matter the buffer we are in.

Try to execute this command:

    :hi link xFoo Bar

Then, in another buffer:

    :syn list xFoo
        xFoo           xxx links to Bar~

Here, `:syn list` tells us that the  syntax group `xFoo` is empty in the current
buffer (because  no item  is reported), but  that if there  were, they  would be
highlighted by the HG `Bar`.

---

Real Example:

    $ vim /tmp/lua.lua
    :e /tmp/py.py
    :syn list luaOperator
        luaOperator    xxx links to Operator~

When Vim has loaded the lua buffer, it has added the HG `luaOperator`.

## `:syn list xFoo` outputs `--- Syntax items ---`.  There's nothing!  What does it mean?

`xFoo` contains no item in the current buffer, and is not associated to a HG.

However, it's mentioned somewhere in a syntax plugin.
It could be in the value passed  to the `matchgroup=` or `contains=` argument of
a syntax item.

IOW, Vim has seen `xFoo` somewhere,  but has no relevant information to provide,
at least in the current buffer.

##
# Priority
## I have 2 conflicting statements
### one uses the subcommand `keyword`, the other `match` or `region`.  Which one wins?

keyword

MWE1:

    syn keyword xKeyword hello
    syn match xMatch /h...o/

    hi link xKeyword DiffAdd
    hi link xMatch   DiffChange

MWE2:

    syn keyword xKeyword hello
    syn region xRegion start=/h/ end=/o/

    hi link xKeyword DiffAdd
    hi link xMatch   DiffChange

In  those 2  examples, even  though `syn  match` and  `syn region`  are executed
*after* `syn keyword`, they are not applied.

### one uses the subcommand `match`, the other `region`.  Which one wins?

The last one.

From `:h syn-priority`:

> 1. When multiple  Match or Region items  start in the same  position, the item
> defined last has priority.

---

In this example, the region is the last one, and so is the one applied to `hello`:

    syn match xMatch /h...o/
    syn region xRegion start=/h/ end=/o/

    hi link xMatch DiffAdd
    hi link xRegion  DiffChange

If you  reverse the order of  `syn match` and  `syn region`, the match  would be
applied instead.

###
## Which of these snippets highlights the operators `-` and `-=`?

    " snippet 1
    syn match xOperator /-=/
    syn match xOperator /-/

    " snippet 2
    syn match xOperator /-/
    syn match xOperator /-=/

    " text
    let foo -= 1
    let bar = foo - 1

↣
You must use the second snippet.
↢

### Why does one work, but not the other?

Suppose you use the first snippet instead.
Both statements match some text in the same position, where the `-` is.

The last statement wins (`:h syn-priority`), and so the syntax plugin highlights `-`.
Now, the remaining text begins with `=`.
But `=` doesn't match any regex used in the 2 statements of the snippet, so it's
left out and not syntax highlighted.

## Which of these statements highlights the integers and floats?

    " statement 1
    syn match xNumber /\d\+\.\d\+\|\d\+/

    " statement 2
    syn match xNumber /\d\+\|\d\+\.\d\+/

    " text
    let foo = 123
    let bar = 123.456

↣
You must use the first statement.
↢

### Why does one work, but not the other?

Suppose you use the second one instead.

The first branch of the regex (`\d\+`) matches `123`.
The latter is highlighted, and the remaining text is `.456`.
This does not match the regex, because the dot is not contained in the latter.
The syntax plugin moves one character forward to skip the dot, and finds `456`.
The latter matches the regex, and so is highlighted.

In the end, `123.456` is highlighted as  2 integers separated by a dot (which is
not highlighted), instead of a single float.

###
## I have 2 items sharing a common prefix.
### I want to describe them with 2 statements.  Which one should describe the longest item?

The last one.

### I want to describe them with 2 branches of a regex.  Which branch should describe the longest item?

The first one.

### Why are these two answers different?

That's how the priority mechanism works.

The *last* statement wins.
The *first* branch wins.

##
# :syn keyword
## 'isk'
### How to print the value of 'isk' local to the syntax plugin?

    syn iskeyword

#### How to reset it?

    syn iskeyword clear

#### If I change its value, what will be affected?

It will affect  whether the keyword passed  to `syn keyword` is  valid, and what
the atom `\k` matches inside a regex passed to `syn match` or `syn region`.

####
### How to add `foo-bar` as a keyword item inside the `xStatement` syntax group?

                  ┌ add the hyphen to the list of recognized keyword characters
                  │
    syn iskeyword -,@,48-57,192-255,$,_

    syn keyword xStatement foo-bar

##
## I wrote `syn keyword xType int`.
### How to tell Vim to ignore the case and treat `Int` and `INT` as if they were `int`?

    syn case ignore

### How to tell Vim to respect the case and treat `Int` and `INT` as if they were NOT `int`?

    syn case match

#### Do these commands affect all statements in a syntax plugin?

No, only the ones afterwards.
And  if another  `syn  case` statement  is  executed later,  the  effect of  the
previous one stops.

#### Which of these commands should I use in my syntax plugin?

It depends on the language you're working on.

If it's case-sensitive, like `C`, use:

    syn case match

If it's case-INsensitive, like `Pascal`, use:

    syn case ignore

##
## How to add the keywords `n`, `ne`, `nex` and `next` inside the `xStatement` syntax group?  (2)

    syn keyword xStatement n ne nex next

    syn keyword xStatement n[ext]

`n[ext]` is a special keyword which is equivalent to the regex:

    \<n\%[ext]\>

##
# :syn match
## What are the four arguments which can't be passed to `:syn match`?

   - `concealends`

   - `matchgroup`

   - `oneline`

   - `start`/`skip`/`end`

The only one which is not obvious is `oneline`.
The others refer to concepts which are specific to a region.

##
## What happens if an item is contained in a match, but it goes on beyond its end?

The containing match is extended until the end of the contained item.

MWE:

    " text
    A c B d xxx

    " syntax plugin
    syn match xContaining /A.\{-}B/
    syn match xContained  /c.\{-}d/ containedin=xContaining

    hi link xContaining DiffAdd
    hi link xContained  DiffChange

The text will be highlighted as follows:

          ┌ xContained
          ├───┐
        A c B d xxx
        ├─────┘
        └ xContaining

The containing match  should stop at `B`  but is extended up to  `d`, because of
the contained item.

### How to prevent this?

Define the containing match with `keepend`.

To return  to the previous  example, if you add  `keepend` in the  definition of
`xContaining`, the text will be highlighted like so:

          ┌ xContained
          ├─┐
        A c B d xxx
        ├───┘
        └ xContaining

This time, the contained item is truncated at the end of the containing match.
And the latter is not extended anymore.

---

You could think  that `keepend` is specific to a  region, because the definition
given at `:h :syn-keepend` mentions the end pattern of a region.
Besides,  there's   only  one  occurrence   of  `:syn  match`  +   `keepend`  in
`$VIMRUNTIME`, and it's commented out:

    :vim /\C\<syn\%[tax]\>.\{-}\<match\>.\{-}\s\zs\<keepend\>\S\@!/gj $VIMRUNTIME/**/*.vim | cw

Nevertheless, `:syn match` *does* accept `keepend`.

Think of it this way, a match also has an end: the anchor `$`.
A contained item can consume it by  not stopping before or at the last character
of the containing match.

##
## Why can't I reliably use `:syn match` to highlight a structure which can contain itself recursively?

Once Vim has found a text matching  the regex passed to `:syn match`, it doesn't
“update” the end of the match.

Consider this:

    " syntax plugin
    syn match xBlock /{.\{-}}/ contains=xBlock
    hi link xBlock DiffAdd

    " text
    foo { bar { baz } qux } norf }
        ^^^^^^^^^^^^^
        highlighted

` qux } norf }` should be highlighted, but it's not.

The outer match stops as soon as it finds a closing `}`.
But when the  syntax plugin finds an  inner block, it doesn't update  the end of
the outer match to the second `}`.
So, all your matches end on the same `}`.

##
# :syn region
## My buffer contains some text matching the beginning of a syntax region, but not its end.  What will be highlighted?

Everything from the beginning of the region until the end of the buffer.

MWE:

    syn region xString start=/"/ end=/"/
    hi link xString DiffAdd

If you source the previous syntax statements while your buffer contains:

    " broken string with missing end quote
    text outside string

`text outside string` will be wrongly highlighted.
That's because once  `:syn region` has found its start,  it doesn't care whether
it can also find its ending.

## How to highlight strings surrounded by `"` withouth considering `\"` as the end of a string?

    syn region xString start=/"/ skip=/\\"/ end=/"/
    hi link xString String

Here's what would be highlighted for the following text:

    before "A string with a double quote (\") in it" after
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you had omitted the `skip` argument:

    before "A string with a double quote (\") in it" after
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       ^^^^^^^

##
## How to conceal the start and end of a region?

Use the `concealends` and `matchgroup` arguments.

`concealends` alone is not enough: the start and end of your region must also be
highlighted by a `matchgroup=SomeSyntaxGroup`.

Example:

    " syntax plugin
    syn region xRegion matchgroup=xMatchGroup start=/A/ matchgroup=NONE end=/B/ concealends
    hi link xRegion DiffAdd
    hi link xMatchGroup DiffChange

    " text
     A foo B bar
     │     │
     │     └ not concealed, because the first `matchgroup=` has been reset
     └ concealed

For more info, see: `:h :syn-concealends`.

##
## matchgroup
### What's its main purpose?

It can be  used to highlight the  start and/or end pattern  differently than the
body of a region.

### What's its side effect?

If the region contains items, they  can't be contained in the start/end patterns
highlighted with a `matchgroup=xMatchgroup`.

MWE:

    " text
    Foo xxx Bar

    " syntax plugin
    syn match xWord /\<...\>/ contained
    syn region xRegion matchgroup=xMatchgroup start=/Foo/ end=/Bar/ contains=xWord

    hi link xRegion      DiffAdd
    hi link xMatchgroup  DiffChange
    hi link xWord        DiffDelete

Notice that when the cursor is on `Foo`, the stack of syntax items is:

    xMatchgroup xRegion~

But without `matchgroup`, it would be:

          xWord xRegion~

---

There's *no* way around this.

Adding `containedin=xMatchgroup` to another item  won't allow it to be contained
in the start/end patterns.

**Nothing can be contained in `xMatchgroup`**.
So, in the previous example, if you had written:

    syn match xWord /\<...\>/ contained containedin=xMatchgroup

And your cursor was on `Foo`, the stack of syntax items would still have been:

          xMatchgroup xRegion~

And not:

    xWord xMatchgroup xRegion~
    ^^^^^

### What happens to the text matched by `end` if it's affected by a `matchgroup=xMatchgroup`?

It's excluded from the region.

In the previous example, you'll notice that when the cursor is on `Bar`, the stack
of syntax items is:

    xMatchgroup~
                ^^^^^^^
                no xRegion

Instead of:

    xMatchgroup xRegion~

### How to limit its effects to the start pattern (not the end one)?

Use an additional `matchgroup=NONE` to reset  to not using a different group for
the end pattern:

                                                          vvvvvvvvvvvvvvv
    syn region xRegion matchgroup=xMatchgroup start=/Foo/ matchgroup=NONE end=/Bar/

    hi link xRegion DiffAdd
    hi link xMatchgroup DiffChange

##
## Which snippet could highlight arbitrarily nested parentheses (with 3 different colors)?

    syn region xPar1 matchgroup=par1 start=/(/ end=/)/ contains=xPar2
    syn region xPar2 matchgroup=par2 start=/(/ end=/)/ contains=xPar3 contained
    syn region xPar3 matchgroup=par3 start=/(/ end=/)/ contains=xPar1 contained

    hi link par1 DiffAdd
    hi link par2 DiffChange
    hi link par3 DiffDelete

You can try it on this text:

    ( one ( two ( three ( four ) five ) six ) seven )
    |     |     |       |      |      |     |       |
    g     m     r       g      g      r     m       g

    g = green
    m = magenta
    r = red

### Why does the snippet need `matchgroup`?

To  prevent the  parentheses  of  a contained  region  from  matching where  the
parentheses of the containing region matched.

### What in the snippet allows Vim to find the right closing parentheses?

The fact that the regions form a cycle:

   1. xPar1 contains xPar2
   2. xPar2 contains xPar3
   3. xPar3 contains xPar1

   4. xPar1 contains xPar2
   ...

If they didn't form a cycle, Vim wouldn't find the right closing parentheses.
The number of regions in a cycle doesn't matter.
Only the existence of a cycle matters.

##
## keepend
### When does a region go further than the first occurrence of a text matching the `end` pattern?

When it  contains an  item which  consumes the text  matching the  `end` pattern
(even partially).

MWE:

    " syntax plugin
    syn region xContained start=/C/ end=/D/ contained
    syn region xRegion start=/ABC/ end=/DEF/ contains=xContained

    hi link xContained DiffAdd
    hi link xRegion    DiffChange

    " text
    foo ABC bar DEF baz

The `xRegion` should stop at `DEF`, but it's extended and highlights ` baz`.

#### What's the rationale behind this unexpected behavior?

It's  necessary  to correctly  highlight  a  region,  which may  contain  itself
recursively.

For example, thanks to this, Vim is able  to correctly find the end of a block
(text surrounded by curly braces), even if it contains another block:

    " syntax plugin
    syn region xBlock start=/{/ end=/}/ contains=xBlock
    hi link xBlock DiffAdd

    " text
    while i < b {
        if a {
            b = c;
        }
    }

Without this behavior,  after finding the first `{`, Vim  would wrongly consider
the  first `}`  it finds  as the  end of  the outer  block, even  if the  latter
contains an inner block.

#### How to prevent this?

Define the region with the `keepend` argument.

##### Are there drawbacks?  (2)

Yes:

   1. the region can't contain itself anymore

   2. if the region contains an item which goes beyond its end,
      the item is truncated

####
### Can a region contain itself by default?

No.

You have to explicitly define it with `contains=xRegion`:

    syn region xBlock start=/{/ end=/}/ contains=xBlock
                                        ^^^^^^^^^^^^^^^

###
### Which issue is created by a region contained inside another region, and with no text matching its end pattern?

It will  go on until the  end of the  containing region, which will  consume the
text matching the end pattern of the latter.
Because of this,  the containing region will  have to look further  for its end,
which is unexpected.
The process will repeat itself, until Vim  finds a text matching the end pattern
of the contained region or until the end of the buffer.

MWE:

    " syntax plugin
    syn region xContained start=/C/ end=/Z/ contained
    syn region xRegion start=/ABC/ end=/DEF/ contains=xContained

    hi link xContained DiffAdd
    hi link xRegion    DiffChange

    " text
    foo ABC bar DEF baz

The `xRegion` should  stop at `DEF`, but it's extended,  as well as `xContained`
which highlights ` baz`.

The solution is, again, to define the containing region with the `keepend` argument.

#### What are the differences between this issue, and the one where a contained item consumes the end of a region?

When a contained item consumes (even partially) the end of its containing region:

   - only the containing region is extended

   - the extended part of the containing region is *completely* highlighted by
     the latter

   - Vim only needs to find a text matching the end pattern of the containing
     region

When a contained region has no end inside the containing region:

   - both the containing region *and* the contained region are extended

   - the extended part of the containing region is highlighted by the contained
     region

    At least until Vim finds an end for the contained region.

   - Vim needs to find *two* texts matching the end pattern of the containing
     region, and of the contained region

#### Consider the following syntax plugin, and the following text:

    " syntax plugin
    syn region xAb start=/a/ end=/b/ contains=xBc
    syn region xBc start=/b/ end=/c/ contained
    hi link xAb DiffAdd
    hi link xBc DiffChange

    " text
     aaa bbb czz
     ├──┘├───┘├┘
     │   │    └ xAb
     │   └ xBc xAb
     └ xAb

##### Why is the region `xAb` extended up to `zz`?

`xBc` consumes the end of `xAb`, and `xBc` doesn't end inside `xAb`.
As a result, both  `xAb` and `xBc` are extended until  their respective ends are
found.
When `c` is found, `xBc` ends, but not `xAb`.
The latter still needs a `b`, which is why `zz` is highlighted by `xAb`.

##### Why is it impossible for the region `xAb` to end, no matter what you write afterwards?

The only way to end `xAb` is to write `b`.
But if you  do, the process will  repeat itself: a new `xBc`  region will start,
which will consume the end of `xAb`, and both will (again) be extended.

###
### I have a region whose end is `$`.  Can a contained item consume it?

Yes.

Think of `$` as the character `<EOL>`.

MWE:

    " text
    do something # some comment
    some command
    another command

    " syntax plugin
    syn match  xComment /#[^#]\+$/
    syn region xCommand start=/do/ end=/$/ contains=xComment
    hi link xComment DiffAdd
    hi link xCommand DiffChange

The `xCommand` region should stop at the end of the first line of the text.
But  it  doesn't,  because  of  the  comment  it  contains  which  consumes  the
end-of-line.
Instead, it goes on until the end of the second line.

### When should I use `keepend` when defining a region?

My guess is: always.

Unless you need to match a recursively nested structure.

---

That's what tpope does in his [markdown syntax plugin][2].
Out of the 24 regions he defines, 22 have `keepend`.
And among the  2 which don't have  it, one doesn't contain any  item, so doesn't
need it:

    syn region markdownCodeBlock start="    \|\t" end="$" contained

The other one is probably an error:

    syn region markdownLinkText matchgroup=markdownLinkTextDelimiter start="!\=\[\%(\_[^]]*]\%( \=[[(]\)\)\@=" end="\]\%( \=[[(]\)\@=" nextgroup=markdownLink,markdownId skipwhite contains=@markdownInline,markdownLineStart

Here, I think he should have added `keepend`, like everywhere else, otherwise in
the following text:

    [*link](http://www.google.com/)

    some text

`some text` is in  italics because `link` is supposed to  be written in italics,
but we forgot the closing star.

##
# Arguments
## contains / containedin
### What do these arguments mean exactly?

`contains=A`  means  that the  item  `A`  is  **allowed  to begin**  inside  the
currently defined item.

`containedin=A` means  that the currently  defined item is **allowed  to begin**
inside `A`.

---

`contains=A` does *not* mean:

>     MUST contain A

And `containedin=A` does *not* mean:

>     MUST be contained in A

### On which condition can a syntax item B start in another A?

Iff either one of these is true:

   - A has `contains=B`

   - B has `containedin=A`

###
### Must a contained item end in the latter?

No.

It only has to *begin* in the containing item.

    " text
    start CCC end ccc

    " syntax plugin
    syn match xContained /C.\{-}c/ contained
    syn region xContaining start=/start/ end=/end/ contains=xContained

    hi link xContained   DiffAdd
    hi link xContaining  DiffChange

In this example, part of the text is matched by a region.
The region contains an item, but the latter does *not* end in the region:

     ┌ initial containing region:
     │ in reality, the region is extended up to the next `end` word
     ├───────────┐
     start CCC end ccc
           ├───────┘
           └ contained match

---

Here's another example, where the containing item is a match instead of a region:

    " text
    start CCC end ccc

    " syntax plugin
    syn match xContained /C.\{-}c/ contained
    syn match xContaining /start.\{-}end/ contains=xContained

    hi link xContained  DiffAdd
    hi link xContaining DiffChange

Again, the contained item ends after the containing one:

     ┌ containing match
     ├───────────┐
     start CCC end ccc
           ├───────┘
           └ contained match

### Are all the characters of an item contained in a region always contained in the latter?

Yes.

Even if  the contained item  consumes the text matching  the end pattern  of the
containing region.
The latter will:

   - be extended if it wasn't defined with `keepend`
   - won't be extended it it was defined with `keepend`

In the latter case, the contained match will be truncated.
In both cases, the contained item is *fully* inside the containing one.

### Are all the characters of an item contained in a match always contained in the latter?

Not necessarily.

MWE:

    " text
    start CCC end ccc

    " syntax plugin
    syn match xContained /C.\{-}c/ contained
    syn match xContaining /start.\{-}end/ contains=xContained

    hi link xContained  DiffAdd
    hi link xContaining DiffChange

The text is matched by the syntax items like so:

     ┌ containing match
     ├───────────┐
     start CCC end ccc
           ├───────┘
           └ contained match

As you can see, ` c` is in the contained match, but *not* in the containing match.

###
### Does `contains=B` mean that B will always be matched inside another item?

No.

B can still be matched at the toplevel.

### How to express that an item MUST be contained in another?

Use the `contained` argument.

###
### How to make an item contain any item which
#### is not `xFoo`, `xBar`, `xBaz`?

    contains=ALLBUT,xFoo,xBar,xBaz

####
#### has the `contained` argument?

    contains=CONTAINED

#### same thing, but excluding `xFoo`, `xBar`, `xBaz`?

    contains=CONTAINED,xFoo,xBar,xBaz

####
#### does *not* have the `contained` argument?

Define it with the argument:

    contains=TOP

#### same thing, but excluding `xFoo`, `xBar`, `xBaz`?

    contains=TOP,xFoo,xBar,xBaz

###
### When should I use `contained`?

All the time.

Unless your item needs to be matched at the toplevel.

### When some text is matched by an item which can be nested, or exist at the toplevel, how does Vim match the text?

Vim will first try to match the text at the toplevel.

---

In this example, `xDot` can be nested inside `xFooBar`, or exist at the toplevel:

    syn match xFooBar /Foo Bar/ contains=xDot
    syn match xDot    /F../

    hi link xFooBar DiffAdd
    hi link xDot    DiffChange

It can be matched at the toplevel because it is not defined with `contained`.

Now, if you try the previous code on this text:

    Foo Bar

` Bar` won't be highlighted according to `xFooBar`.
It won't be highlighted at all.

This is because:

   1. the last statement wins, so `Foo` is highlighted by `syn match xDot`

   2. Vim tries to match `Foo` at the top level first
   (before trying to match it inside `xFooBar`)

The remaining text is ` Bar` which doesn't match the regex of `xFooBar`.

### Why should I write the statement describing a containing item *after* the one of the contained item?

If you  write the  statement describing  the containing item  first, and  if the
contained item  can match at  the beginning of  the containing one,  then you'll
have to use `contained`.

Otherwise, they containing item would be broken.
For an example, see the previous question.

But because of `contained`, your contained item has no longer the possibility to
match at the toplevel.

By writing the statement of the containing item *after* the one of the contained item:

   - you don't have to remember this peculiarity

   - your contained item still has the possibility to match at the toplevel

##
## transparent
### What's its main purpose?

The item will *not*  be highlighted itself, but will take  the highlighting of the
item it is contained in.

This is useful  for syntax items that  don't need any highlighting  but are used
only to skip over a part of the text.

###
### Which pitfall could I face when using `transparent`?

By definition, a transparent item is contained in another one.
Let's call it `A`.
If other items can be contained in `A` (via `contains=` or `containedin=`), they
can also be  contained in the transparent  item, even if it  wasn't defined with
`contains=`.

As a result,  a transparent item could contain another  item, and be highlighted
according to the latter instead of the containing item.

It's as if you had put a transparent window in your house to see the garden, but
someone put a sticker on it.
You can't see your garden from the part of the window where the sticker is.

#### How to avoid it?

If you don't want your transparent item to contain any undesired item, define it
with the `contains=NONE` argument.

Example:

    syn match xVim /\<vim\>/ transparent contained contains=NONE
                                                   ^^^^^^^^^^^^^

###
### Here is a usage example of `transparent`:

It highlights words in strings, but makes an exception for the word `vim`:

    $ echo "'foo vim bar'" >/tmp/file

    $ cat <<'EOF' >/tmp/vimrc
    syn match xString /'[^']*'/    contains=xWord,xVim
    syn match xWord   /\<[a-z]*\>/ contained
    syn match xVim    /\<vim\>/    contained contains=NONE transparent

    hi link xString String
    hi link xWord   Comment

    syntax on
    EOF

    $ vim -Nu /tmp/vimrc /tmp/file

Result:

     'foo vim bar'
     |||| ||| ||||
     rbbb rrr bbbr
     │  │
     │  └ blue
     └ red

Since the `xVim` match comes after `xWord` it is the preferred match (last match
in the same position overrules an earlier one).
And the `transparent` argument makes the  `xVim` match use the same highlighting
as `xString`.

Note that without  `contains=NONE`, `xVim` would have  inherited the `contains=`
argument from `xString` and allowed `xWord` to be contained.
As a result, the match (`vim`) would  have been highlighted as a comment instead
of a string.

### In this example, what would have been the stack of items on the `vim` word, if I had executed:
#### `syn match xVim /\<vim\>/ contained`?

    xVim xString

Not highlighted, because no HG is linked to `xVim`.

#### `syn match xVim /\<vim\>/ contained transparent`?

    xWord xVim xString

Highlighted as a comment.

---

Why doesn't the command produce this stack:

    xVim xWord xVim xString
    ^^^^

Well,  I  don't  think  it's  possible  because  `xWord`  is  not  defined  with
`contains=xVim`, but even if it was, according to `:h syn-transparent`:

> ... a contained  match doesn't match inside itself in  the same position, thus
> the "xVim" match doesn't overrule the "xWord" match here.

The first match due to `xVim` is contained in a syntax item (`xString`).
As a result,  it can't be used to  match inside itself a second  time **in the**
**same position**.

#### `syn match xVim /\<vim\>/ contained transparent contains=NONE`?

        xVim xString

Highlighted as a string because of `transparent`.

Note that `transparent` only affects the highlighting.
It doesn't make `xVim` disappear.
But it would make “disappear” its HG if it was linked to any.
IOW, if you had used this statement in the previous example:

    hi link xVim Title

`vim` would still have been highlighted as a comment, not a title.

###
### If I use `transparent` and `matchgroup` in a region definition, will the start and end patterns be transparent?

Not all of them.

The ones  which are preceded  by a `matchgroup=xMatchgroup` will  be highlighted
according to `xMatchgroup`.

MWE:

    syn match xLine /.*/ contains=xRegion
    syn region xRegion matchgroup=xMatchgroup start=/Foo/ end=/Bar/ transparent

    hi link xLine        DiffAdd
    hi link xRegion      DiffChange
    hi link xMatchgroup  DiffDelete

Here, even though the region should be transparent, only its body will be.
`Foo` and `Bar` will be highlighted according to `xMatchgroup`, not `xLine`.

##
# Highlight Group
## Do I have to define a HG for each syntax group?

No, Vim does it automatically.

    :syn match xFoo /pat/

This command creates the syntax group `xFoo` *and* the HG `xFoo`.

## How to change the color of a syntax item?

Re-link its HG to another HG.

For example, if  you don't like the  color of fold titles in  a markdown buffer,
you could execute:

    :hi! link markdownH2 DiffAdd

## How to prevent a syntax item from being highlighted by its HG?

Clear its HG.

If the HG is linked to another, write this in `~/.vim/after/sytax/x.vim`:

    :hi link xFoo NONE

If the HG is *not* linked to another, write this instead:

    :hi clear xFoo
              │
              └ name of the HG to which the item is linked

---

But don't do that:

    :syn clear xFoo

The text could still be highlighted by another item which contains it.
And the  removal of  `xFoo` could  break other  syntax items  which rely  on its
existence (via a `containedin=xFoo` argument for example).

For more info, see: <https://vi.stackexchange.com/a/17445/17449>

## What does `def` mean in `hi def link cComment Comment`?

`def[ault]` means  that the  HG is only  to be used  as a  fallback/default when
`cComment` has not already been linked to a HG.

IOW, it tells Vim  to ignore the statement if `cComment` is  already linked to a
HG.
This allows the user to choose another HG.
For example, if they write in their vimrc:

    :hi link cComment Question

A comment in a  `C` file would be highlighted with the  `Question` HG instead of
the `Comment` one.

For more info, see:

    :h hi-default

##
# Issues
## My statements are correct.  But sometimes, they fail to highlight a line!

Temporarily increase the value of `'smc'`.
If the line is immediately highlighted  correctly, the issue comes from the line
being too long.
Try to reduce its length.

We assign the value `250` to `'smc'` which should be more than enough for any line.

---

An example of this issue occurs when you draw a wide table.

If you use multi-byte characters to draw a table, an edge line will have a big weight.
It may exceed `&smc`, and make the line highlighted as a comment instead of a table.

## My syntax item has a negative impact on Vim's performance!

If you use a match, and the regex is too complex, try a region.

---

Avoid lookarounds (especially lookbehinds) as much as possible.
Avoid quantifiers inside lookarounds as much as possible.

---

If you wrote something like this:

         *
    ^^^^^
    spaces

Try this instead:

     \{5,}
    ^
    space

This had a big impact on the performance of `xCommentOutput`.

##
##
##
# usr_44
## 5 nested items
### Containing Many Items

You can use the contains argument to specify that everything can be contained.
For example:

    syn region xList start=/\[/ end=/\]/ contains=ALL

All syntax items will be contained in this one.
It also  contains itself,  but not  at the  same position  (that would  cause an
endless loop).
You can specify that some groups are not contained.
Thus contain all groups but the ones that are listed:

    syn region xList start=/\[/ end=/\]/ contains=ALLBUT,xString

With the  "TOP" item  you can include  all items that  don't have  a "contained"
argument.
"CONTAINED" is used to only include items with a "contained" argument.
See |:syn-contains| for the details.

##
## 6 Following groups

The x language has statements in this form:

    if (condition) then

You want to highlight the three items differently.
But "(condition)" and  "then" might also appear in other  places, where they get
different highlighting.
This is how you can do this:

    syn match xIf           /if/       nextgroup=xIfCondition     skipwhite
    syn match xIfCondition  /([^)]*)/  contained nextgroup=xThen  skipwhite
    syn match xThen         /then/     contained

The "nextgroup" argument specifies which item can come next.
This is not required.
If none of the items that are specified are found, nothing happens.
For example, in this text:

    if not (condition) then

The "if" is matched by xIf.
"not" doesn't match the specified nextgroup  xIfCondition, thus only the "if" is
highlighted.

The "skipwhite" argument tells Vim that white space (spaces and tabs) may appear
in between the items.
Similar arguments are "skipnl", which allows  a line break in between the items,
and "skipempty", which allows empty lines.
Notice that "skipnl" doesn't skip an  empty line, something must match after the
line break.

##
## 7 Other arguments
### Matchgroup

When you  define a  region, the  entire region is  highlighted according  to the
group name specified.
To highlight  the text enclosed  in parentheses ()  with the group  xInside, for
example, use the following command:

    syn region xInside start=/(/ end=/)/

Suppose, that you want to highlight the parentheses differently.
You can do this  with a lot of convoluted region statements, or  you can use the
"matchgroup" argument.
This tells  Vim to  highlight the  start and end  of a  region with  a different
highlight group (in this case, the xParen group):

    syn region xInside matchgroup=xParen start=/(/ end=/)/

The "matchgroup" argument applies to the start or end match that comes after it.
In the previous example both start and end are highlighted with xParen.
To highlight the end with xParenEnd:

    syn region xInside matchgroup=xParen start=/(/
        \ matchgroup=xParenEnd end=/)/

A side effect  of using "matchgroup" is  that contained items will  not match in
the start or end of the region.
The example for "transparent" uses this.

### Transparent

In a  C language file you  would like to highlight  the () text after  a "while"
differently from the () text after a "for".
In both of  these there can be  nested () items, which should  be highlighted in
the same way.
You must make sure the () highlighting stops at the matching ).
This is one way to do this:

    syn region cWhile matchgroup=cWhile start=/while\s*(/ end=/)/
        \ contains=cCondNest
    syn region cFor matchgroup=cFor start=/for\s*(/ end=/)/
        \ contains=cCondNest
    syn region cCondNest start=/(/ end=/)/ contained transparent

Now you can give cWhile and cFor different highlighting.
The cCondNest item can appear in either  of them, but take over the highlighting
of the item it is contained in.
The "transparent" argument causes this.
Notice that the "matchgroup" argument has the same group as the item itself.
Why define it then?
Well, the  side effect  of using a  matchgroup is that  contained items  are not
found in the match with the start item then.
This avoids  that the cCondNest  group matches the (  just after the  "while" or
"for".
If this would happen,  it would span the whole text until  the matching) and the
region would continue after it.
Now cCondNest  only matches after the  match with the start  pattern, thus after
the first (.

### Offsets

Suppose you want to define a region for the text between ( and ) after an "if".
But you don't want to include the "if" or the ( and ).
You can do this by specifying offsets for the patterns.
Example:

    syn region xCond start=/if\s*(/ms=e+1 end=/)/me=s-1

The offset for the start pattern is "ms=e+1".
"ms" stands for Match Start.
This defines an offset for the start of the match.
Normally the match starts where the pattern matches.
"e+1" means that the match now starts at  the end of the pattern match, and then
one character further.
The offset for the end pattern is "me=s-1".
"me" stands for Match End.
"s-1" means the start of the pattern match and then one character back.
The result is that in this text:

    if (foo == bar)

Only the text "foo == bar" will be highlighted as xCond.

More about offsets here: |:syn-pattern-offset|.

### Oneline

The "oneline" argument indicates that the region does not cross a line boundary.
For example:

    syn region xIfThen start=/if/ end=/then/ oneline

This defines a region that starts at "if" and ends at "then".
But if there is no "then" after the "if", the region doesn't match.

Note:

When using "oneline"  the region doesn't start if the  end pattern doesn't match
in the same line.
Without "oneline" Vim does _not_ check if there is a match for the end pattern.
The region  starts even when the  end pattern doesn't  match in the rest  of the
file.

---

When should I use `oneline`?

Read `:h :syn-oneline`.

### Continuation Lines And Avoiding Them

Things now become a little more complex.
Let's define a preprocessor line.
This starts with  a `#` in the first  column and continues until the  end of the
line.
A line that ends with `\` makes the next line a continuation line.
The way you  handle this is to  allow the syntax item to  contain a continuation
pattern:

    syn region xPreProc      start=/^#/ end=/$/ contains=xLineContinue
    syn match  xLineContinue "\\$"              contained

In this  case, although  `xPreProc` normally  matches a  single line,  the group
contained in it (namely `xLineContinue`) lets it go on for more than one line.
For example, it would match both of these lines:

    #define SPAM  spam spam spam \
            bacon and spam

In this case, this is what you want.
If it is not what  you want, you can call for the region to  be on a single line
by adding `excludenl` to the contained pattern.
For example, you want  to highlight `end` in `xPreProc`, but only  at the end of
the line.
To avoid making  the `xPreProc` continue on the next  line, like `xLineContinue`
does, use `excludenl` like this:

    syn region xPreProc start=/^#/ end=/$/
        \ contains=xLineContinue,xPreProcEnd
    syn match xPreProcEnd excludenl  /end$/  contained
    syn match xLineContinue          "\\$"   contained

`excludenl` must be placed before the pattern.
Since  `xLineContinue` doesn't  have `excludenl`,  a match  with it  will extend
`xPreProc` to the next line as before.

##
## 8 Clusters

One of the  things you will notice as  you start to write a syntax  file is that
you wind up generating a lot of syntax groups.
Vim enables you to define a collection of syntax groups called a cluster.
Suppose you have a language that contains for loops, if statements, while loops,
and functions.
Each of them contains the same syntax elements: numbers and identifiers.
You define them like this:

    syn match xFor    /^for.*/    contains=xNumber,xIdent
    syn match xIf     /^if.*/     contains=xNumber,xIdent
    syn match xWhile  /^while.*/  contains=xNumber,xIdent

You have to repeat the same `contains=` every time.
If you want to add another contained item, you have to add it three times.
Syntax clusters simplify  these definitions by enabling you to  have one cluster
stand for several syntax groups.
To define  a cluster for the  two items that  the three groups contain,  use the
following command:

    syn cluster xState contains=xNumber,xIdent

Clusters are used inside other syntax items just like any syntax group.
Their names start with `@`.
Thus, you can define the three groups like this:

    syn match xFor    /^for.*/    contains=@xState
    syn match xIf     /^if.*/     contains=@xState
    syn match xWhile  /^while.*/  contains=@xState

You can add new group names to this cluster with the `add` argument:

    syn cluster xState add=xString

You can remove syntax groups from this list as well:

    syn cluster xState remove=xNumber

## 9 Including another syntax file

The C++ language syntax is a superset of the C language.
Because you do not  want to write two syntax files, you can  have the C++ syntax
file read in the one for C by using the following command:

    runtime! syntax/c.vim

`:runtime!` searches `'runtimepath'` for all `syntax/c.vim` files.
This makes the C parts of the C++ syntax be defined like for C files.
If you have replaced  the c.vim syntax file, or added items  with an extra file,
these will be loaded as well.
After loading the C syntax items the specific C++ items can be defined.
For example, add keywords that are not used in C:

    syn keyword cppStatement    new delete this friend using

This works just like in any other syntax file.

Now consider the Perl language.
A Perl  script consists of  two distinct parts:  a documentation section  in POD
format, and a program written in Perl itself.
The POD section starts with `=head` and ends with `=cut`.
You want to define  the POD syntax in one file, and use  it from the Perl syntax
file.
The `:syntax include` command reads in a  syntax file and stores the elements it
defined in a syntax cluster.
For Perl, the statements are as follows:

    syn include @Pod <sfile>:p:h/pod.vim
    syn region perlPOD start=/^=head/ end=/^=cut/ contains=@Pod

When `=head` is found in a Perl file, the perlPOD region starts.
In this region the `@Pod` cluster is contained.
All the items defined as top-level items  in the pod.vim syntax files will match
here.
When `=cut` is found, the region ends and we go back to the items defined in the
Perl file.
The  `:syntax include`  command is  clever enough  to ignore  a `:syntax  clear`
command in the included file.
And an  argument such as `contains=ALL`  will only contain items  defined in the
included file, not in the file that includes it.
The `<sfile>:p:h/` part  uses the name of the current  file (`<sfile>`), expands
it to a full path (`:p`) and then takes the head (`:h`).
This results in the directory name of the file.
This causes the `pod.vim` file in the same directory to be included.

## 10 Synchronizing

Compilers have it easy.
They start at the beginning of a file and parse it straight through.
Vim does not have it so easy.
It must start in the middle, where the editing is being done.
So how does it tell where it is?
The secret is the `:syntax sync` command.
This tells Vim how to figure out where it is.
For example, the following command tells  Vim to scan backward for the beginning
or end of a C-style comment and begin syntax coloring from there:

    syn sync ccomment

You can tune this processing with some arguments.
The `minlines` argument tells Vim the  minimum number of lines to look backward,
and `maxlines` tells the editor the maximum number of lines to scan.
For example, the  following command tells Vim  to look at least  10 lines before
the top of the screen:

    syn sync ccomment minlines=10 maxlines=500

If it cannot figure out where it is in that space, it starts looking farther and
farther back until it figures out what to do.
But it looks no farther back than 500 lines.
A large `maxlines` slows down processing.
A small one might cause synchronization to fail.
To  make synchronizing  go a  bit faster,  tell Vim  which syntax  items can  be
skipped.
Every match and region that only needs  to be used when actually displaying text
can be given the `display` argument.
By default,  the comment to be  found will be  colored as part of  the `Comment`
syntax group.
If you  want to  color things another  way, you can  specify a  different syntax
group:

    syn sync ccomment xAltComment

If your programming language  does not have C-style comments in  it, you can try
another method of synchronization.
The simplest  way is  to tell Vim  to space back  a number  of lines and  try to
figure out things from there.
The following  command tells  Vim to go  back 150 lines  and start  parsing from
there:

    syn sync minlines=150

A  large  `minlines`  value  can  make Vim  slower,  especially  when  scrolling
backwards in the file.
Finally, you can specify a syntax group to look for by using this command:

    syn sync match {sync-group-name}
        \ grouphere {group-name} {pattern}

This  tells  Vim   that  when  it  sees  `{pattern}`  the   syntax  group  named
`{group-name}` begins just after the pattern given.
The  `{sync-group-name}`  is  used  to  give  a  name  to  this  synchronization
specification.
For example, the sh scripting language begins an if statement with `if` and ends
it with `fi`:

    if [ --f file.txt ] ; then
        echo "File exists"
    fi

To  define a  `grouphere`  directive  for this  syntax,  you  use the  following
command:

    syn sync match shIfSync grouphere shIf "\<if\>"

The `groupthere` argument tells Vim that the pattern ends a group.
For example, the end of the `if`/`fi` group is as follows:

    syn sync match shIfSync groupthere NONE "\<fi\>"

In this  example, the `NONE` tells  Vim that you  are not in any  special syntax
region.
In particular, you are not inside an `if` block.

You  also  can define  matches  and  regions that  are  with  no `grouphere`  or
`groupthere` arguments.
These groups are for syntax groups skipped during synchronization.
For example,  the following skips  over anything inside  `{}`, even if  it would
normally match another synchronization method:

    syn sync match xSpecial /{.*}/

More about synchronizing in the reference manual: |:syn-sync|.

##
## 11 Installing a syntax file
### Adding To An Existing Syntax File

We were assuming you were adding a completely new syntax file.
When an existing syntax file works, but is missing some items, you can add items
in a separate file.
That  avoids changing  the  distributed syntax  file, which  will  be lost  when
installing a new version of Vim.
Write syntax commands in your file, possibly using group names from the existing
syntax.
For example, to add new variable types to the C syntax file:

    syn keyword cType off_t uint

Write the file with the same name as the original syntax file.
In this case `c.vim`.
Place it in a directory near the end of `'runtimepath'`.
This makes it loaded after the original syntax file.
For Unix this would be:

    ~/.vim/after/syntax/c.vim

##
## 12 Portable syntax file layout

Wouldn't it be nice if all Vim users exchange syntax files?
To make this possible, the syntax file must follow a few guidelines.

Start with a header that explains what  the syntax file is for, who maintains it
and when it was last updated.
Don't include too  much information about changes history, not  many people will
read it.
Example:

    " Vim syntax file
    " Language: C
    " Maintainer:   Bram Moolenaar <Bram@vim.org>
    " Last Change:  2001 Jun 18
    " Remark:   Included by the C++ syntax.

Use the same layout as the other syntax files.
Using an existing syntax file as an example will save you a lot of time.

Choose a good, descriptive name for your syntax file.
Use lowercase letters and digits.
Don't make it too  long, it is used in many places: The name  of the syntax file
`name.vim`, `'filetype'`, `b:current_syntax` and the  start of each syntax group
(`nameType`, `nameStatement`, `nameString`, etc).

Start with a check for `b:current_syntax`.
If it is defined, some other syntax file, earlier in `'runtimepath'` was already
loaded:

    if exists('b:current_syntax')
        finish
    endif

Set `b:current_syntax` to the name of the syntax at the end.
Don't  forget  that  included  files  do  this too,  you  might  have  to  reset
`b:current_syntax` if you include two files.

Do not include anything that is a user preference.
Don't set `'tabstop'`, `'expandtab'`, etc.  These belong in a filetype plugin.

Do not include mappings or abbreviations.
Only  include setting  `'iskeyword'` if  it  is really  necessary for  recognizing
keywords.

To allow  users select their own  preferred colors, make a  different group name
for every kind of highlighted item.
Then link each of them to one of the standard highlight groups.
That will make it work with every color scheme.
If you select specific colors it will look bad with some color schemes.
And don't forget that some people use a different background color, or have only
eight colors available.

For  the linking  use `:hi  def link`,  so that  the user  can select  different
highlighting before your syntax file is loaded.
Example:

      hi def link nameString    String
      hi def link nameNumber    Number
      hi def link nameCommand   Statement
      ... etc ...

Add the `display` argument to items that  are not used when syncing, to speed up
scrolling backwards and `C-l`.

##
# Sh: Embedding Languages

You may wish to embed languages into sh.
I'll give an example  courtesy of Lorance Stinson on how to do  this with awk as
an example.
Put the following file into `~/.vim/after/syntax/sh/awkembed.vim`:

    " AWK Embedding:
    "
    " Shamelessly ripped from aspperl.vim by Aaron Hope.
    if exists("b:current_syntax")
      unlet b:current_syntax
    endif
    syn include @AWKScript syntax/awk.vim
    syn region AWKScriptCode matchgroup=AWKCommand start=+[=\\]\@<!'+ skip=+\\'+ end=+'+ contains=@AWKScript contained
    syn region AWKScriptEmbedded matchgroup=AWKCommand start=+\<awk\>+ skip=+\\$+ end=+[=\\]\@<!'+me=e-1 contains=@shIdList,@shExprList2 nextgroup=AWKScriptCode
    syn cluster shCommandSubList add=AWKScriptEmbedded
    hi def link AWKCommand Type

This code will then let the awk code in the single quotes:

    awk '...awk code here...'

be highlighted using the awk highlighting syntax.
Clearly this may be extended to other languages.

##
##
##
# TODO
## ?

Document `:h :syn-spell` and `:h spell-syntax`.

## ?

Document that a cluster may have the same name than a group.
There seems to be no conflict.
Maybe because a cluster name is always prefixed by `@`.

## ?

Document that you should never use `contains=TOP`.
It breaks  the syntax  highlighting when the  syntax plugin is  used to  embed a
language inside another.

See here for a solution:
<https://github.com/derekwyatt/vim-scala/pull/59>
<https://github.com/vim-pandoc/vim-pandoc-syntax/issues/54>

---

Document that you can't clear a syntax group in `~/.vim/after/syntax/x.vim` when
the syntax plugin is sourced by `:syn include`.

MWE:

    $ echo 'syn clear zshBrackets' >>~/.vim/after/syntax/zsh.vim

    $ cat <<'EOF' >/tmp/md.md
    ```zsh
    func() {
      local var="123"
    }
      local var="123"
    ```
    EOF

    $ vim -Nu NONE \
      +'syntax on' \
      +'let g:markdown_fenced_languages=["zsh"]' \
      +'breakadd file */syntax/zsh.vim' \
      +'breakadd file */syntax/zsh/*.vim' \
      /tmp/md.md
    :e
    >f
    >n
    >syn list zshBrackets

The output of the last command should be empty, but it's not.

Theory: maybe the syntax group is locked while the cluster is defined...

Solution:
Clear (then customize if you want) the syntax group from an autocmd listening to `Syntax`.

    augroup syntax_fix_embedding
        au!
        au Syntax markdown call s:fix_embedding()
    augroup END

    fu s:fix_embedding() abort
        if execute('syn list @markdownEmbedzsh', 'silent!') !~# 'markdownEmbedzsh'
            return
        endif
        syn clear zshBrackets
    endfu

## ?

Whenever you've used a positive lookaround  at the beginning/end of an item, try
to use an offset instead.
It may improve the performance.
But it's only possible  if you can know the length of  the lookaround in advance
(so no quantifier inside).

## ?

Document how to quickly debug some syntax highlighting code:

    $ cat <<'EOF' >/tmp/file
    some text
    EOF

    $ cat <<'EOF' >/tmp/vimrc
    syn clear

    syn ...
    ...

    hi ...
    ...

    augroup debug_syntax
      au!
      au CursorMoved <buffer> echo join(reverse(map(synstack(line('.'), col('.')), {_,v -> synIDattr(v, 'name')})))
      au BufEnter <buffer> so /tmp/vimrc
    augroup END
    EOF

    $ vim /tmp/file

## ?

Conceal and highlight links in comments (all filetypes).

Example:

    [commit 8.1.0560](https://github.com/vim/vim/releases/tag/v8.1.0560)

We will have to tweak `vim-gx` to open links such as:

    [commit 8.1.0560][1]
    [1]: https://github.com/vim/vim/releases/tag/v8.1.0560

It works in a markdown buffer (but don't indent the text), but not in a Vim one.
Study how it works in markdown.

## ?

Document that when two syntax items match  the same text, you must write the one
with the most detailed description last.

That's why we must define the italic,  bold, bold+italic styles in this order in
our markdown syntax plugin (same thing for our comments).

If you  don't want  to respect  any particular  order, you'll  have to  use more
detailed descriptions  (i.e. more  complex regexes, possibly  with lookarounds),
which may have an undesired impact on performance.

## ?

   - some list item 1
   - some list item 2
   - some list item 3

*   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
    Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,
    viverra nec, fringilla in, laoreet vitae, risus.
*   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.
    Suspendisse id sem consectetuer libero luctus adipiscing.


*    Lorem ipsum dolor sit amet, consectetuer adipiscing
elit. Aliquam hendrerit mi posuere lectus. Vestibulum enim
wisi, viverra nec, fringilla in, laoreet vitae, risus.
*   Donec sit amet nisl. Aliquam semper ipsum sit amet
velit. Suspendisse id sem consectetuer libero luctus
adipiscing.


1.  This is a list item with two paragraphs. Lorem ipsum dolor sit amet,
    consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.

    Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
    Donec sit amet nisl.
    Aliquam semper ipsum sit amet velit.

2. Suspendisse id sem consectetuer libero luctus adipiscing.


*   This is a list item with two paragraphs. This
is the second paragraph in the list item.
You're only required to indent the first line. Lorem
ipsum dolor sit amet, consectetuer adipiscing elit.

*   Another item in the same list.

*   A list item with a code block:

        <code goes here>

    the item goes on here

*   A list item with a blockquote:

    > This is a blockquote
    > inside a list item.

    the item goes on here

Some text outside a list.

 > This is a blockquote
 > outside a list item.

---

- *item

some text
some text

Make sure `some text` is not in blue and italics.

---

Also, write this:

- item1
- ** foo `item2` bar**
- item3

Make sure the next lines are not highlighted as list items.

---

Also, write this:

- item1
- **foo `item2` bar**
- item3

Make sure the backticks around `item2` are concealed.

Make sure your solution works in other filetypes.

## ?

Document that it's a bad idea to use quantifiers such as `*` inside a lookbehind
(bad perf),  but that you  can mitigate the  issue by limiting  the backtracking
(`\@123<=`, `\@123<!`).

Maybe recommend to avoid quantifiers in lookaround (including lookafter).

---

Also, document that you can test the performance of your regex with:

    :syntime clear
    :syntime on

    move around

    :syntime off
    :syntime report

Maybe move the section `syntax plugin` from ./debug.md.

Also,  document the  tips given  at the  end of  `:h syntime`,  to increase  the
performance of the regexes.

## ?

Document that in a Vim syntax statement, `foo\zs` and `\zebar` consume `foo` and
`bar`.
It means  that if  you need to  apply some  style to `foo`  or `bar`  in another
statement, you can't use `\zs` and `\ze`.
Instead, use `\<@=` and `\@=`.

This is confirmed in this answer:
<https://stackoverflow.com/a/53730038/9780968>

> Another pitfall is that \zs limits the highlighting, but internally still matches the whole text.

Update:
I think `\zs` and `\ze` are significantly faster.
Maybe we should learn more about syntax to use them, and deal with the “consuming”;
using nested items or something like that...

## ?

Review `vim-comment`.
Do we need `gC` and `iC`?
Adapt their code when necessary.

## ?

Check all styles work as expected in all desired filetypes:

    # Note: text
    # TODO: text

    * emphasis *
    ` codespan `
    ** strong **

    # * emphasis *
    # ` codespan `
    # ** strong **

    ( * NO emphasis *
    ( ` NO codespan `
    ( ** NO strong **

        codeblock
        # commented codeblock

    > blockquote
    > * emphasis *
    > ` code span `
    > ** strong **

Replace `#` with the right comment leader for each tested filetype.

## ?

Have a look at our vimrc, look for `PA` and `PQ` (near our 16th `TO_DO`).
Note that the diagram is misaligned.
Maybe  you  should   create  a  mapping  which  would   add  characters  (exotic
whitespace?) which  would be concealed, so  that the diagram stays  aligned with
what it's supposed to refer to when we press `coc`.

## ?

    $ cat <<'EOF' >/tmp/vimrc

    syn clear

    syn region xFor      matchgroup=xFor   start='for\s*('   end=')' contains=xCondNest
    syn region xWhile    matchgroup=xWhile start='while\s*(' end=')' contains=xCondNest
    syn region xCondNest                   start='('         end=')' contained transparent

    hi link xFor      DiffAdd
    hi link xWhile    DiffChange
    hi link xCondNest DiffDelete
    EOF

    $ cat <<'EOF' >/tmp/file

    for (i=0; i <= (a+b); i++) {
       statement(s);
    }

    while (i <= (a+b)) {
       statement(s);
    }
    EOF

    $ vim /tmp/file
    :so /tmp/vimrc

Press `!s` on `for` or `while`.
The stack contains 2 identical items (`xFor`, or `xWhile`).
Document why.

Hint:
The contained item describes the `start` match.
The containing item describes the match due to the whole region.

## ?

    $ echo 'one two three' >/tmp/file

    $ cat <<'EOF' >/tmp/vimrc
    syn region xRegion matchgroup=xMatchgroup start='one' end='three'
    hi link xRegion DiffAdd
    hi link xMatchgroup DiffChange
    EOF

    $ vim /tmp/file

Press `!s`  on `three`,  and you'll see  that the stack  of items  only contains
`xMatchgroup`.
It doesn't contain `xRegion` which  seems to indicate that `matchgroup=` removes
the `end` match from a region.

## ?

Document the arguments:

   - display
   - excludenl
   - extend
   - fold

## ?

We wrote that we should always use `keepend` when defining a region.

What about a match?
In `$VIMRUNTIME`, no one use `keepend` with `:syn match`.
And yet, I found one example where it's needed to prevent a bug:

    syn match markdownListItem ... keepend

Btw, the description given at `:h :syn-match` is copied from the one
at `:h :syn-region`, and doesn't make sense in the context of a match:

> keepend
>
> Don't allow contained matches to go past a match with the end pattern.

## ?

Document `:h :syn-sync`.

## ?

Document `:h :syn-pattern-offset`.

## ?

Document the special group `ALL` (`:h syn-contains`).
Explain why you should avoid it.

Also document `ALLBUT`.
Explain why it's a dangerous value in a default syntax plugin.
You have to customize the latter  in `after/syntax/x.vim`, to make sure all your
custom groups are excluded from a default syntax group.
Read our comments above the statement:

    call s:define_cluster(filetype)

inside `lg#styled_comment#syntax()`

## ?

Document `:h synconcealed()`.

## ?

    " syntax plugin
    syn match xBlock /{\_.\{-}}/ contains=xBlock
    hi link xBlock DiffAdd

    " text
    foo { bar { baz { qux } } }

When I'm trying the previous statement, and make some modification:

   - reload the buffer
   - add/remove an argument
   - focus another buffer and get back
   - temporarily switch to a region with `:syn region` then get back to `:syn match`

the highlighting is broken in some locations.
And `synstack()` doesn't report anything in some other locations even though the
text is highlighted under the cursor.

These issues only occur with the first multi-line text, not with single line one.

`=d` seems to fix them.
It may be a  problem of synchronizing... Or we should never  use `:syn match` to
highlight a multi-line text, and prefer `:syn region`.

Besides, it seems that `:syn match` is rarely used to match a multi-line text in
`$VIMRUNTIME`:

    :noa vim /\C\<syn\%[tax]\>\s\+match\>.*\%(\\n\|\\_\.\)/gj $VIMRUNTIME/**/*.vim | cw

    " not interested in the literal 2 characters `\` and `n`
    :Cfilter! \\\@<!\\\\n

    " not interested in a negated collection containing `\n`
    :Cfilter! \[\^[^\]]*\\n[^\]]*\]

## ?

This  is an  old comment  we  wrote in  `lg#styled_comment#syntax()`, which  has
become irrelevant after a refactoring.
Nonetheless,  I  keep  it here,  so  that  you  read  it and  see  whether  some
information should be turned in question/answer.

---

Warning: Do *not* use `\zs` instead of `\%(...\)\@<=`!

It would sometimes break `xCommentCodeBlock`.

MWE:

    $ echo ' #    codeblock' >/tmp/awk.awk
            ^
            ✘ indentation breaks syntax

    $ vim /tmp/awk.awk

The text `#    codeblock` is not properly highlighted.

Why?
The beginning of a nested item must be inside the containing item.
From `:h syn-contains`:

>     These groups will be allowed to begin **inside** the item...

In particular,  a nested item can  *not* begin before the  containing item
has begun.

If you use `\zs`, `xCommentCodeBlock`  will start right from the beginning
of the line, because the regex starts with the anchor `^`.
Yes, `\zs` doesn't change the start of the item.

But `xCommentCodeBlock` is supposed to be contained in `xComment`.
OTOH, `xComment` may sometimes begin *after* the beginning of the line.

Example:

    syn match awkComment "#.*" contains=@Spell,awkTodo

Here, `awkComment` doesn't start at the  beginning of the line, but at the
comment leader.
As  a  result, if  your  comment  is indented  (i.e.  there's  at least  1
space between  the beginning  of the  line and  the comment  leader), then
`xCommentCodeBlock` will start *before* `xComment`.

## ?

some **bold** text
some [url *text*](http://www.google.com)
some **bold *foo* bar** text

---

Which combination of styles should our comments and markdown notes support?

First, which styles do we currently support?

   - blockquote
   - list
   - table
   - url

   - bold
   - italic
   - bold+italic
   - option
   - pointer
   - key
   - output
   - codespan
   - codeblock

The first group of styles can contain other styles.
The second group can't (sure?).

There won't be any style in:

   - table      (the conceal would break its alignment)
   - codespan   (no style in code)
   - codeblock  (")
   - output     (")
   - pointer    (doesn't make sense to style a pointer)
   - option     (")

Which gives the following combinations:

   - bold + url
   - italic + url
   - bold+italic + url

   - blockquote + bold + url
   - blockquote + italic + url
   - blockquote + bold+italic + url

   - list + bold + url
   - list + italic + url
   - list + bold+italic + url

In the future we could add `strings` and `tags`.

Update:

We should support the `output` style inside a list item, inside comments.

Update:

Forget about *all* possible combinations.
There are probably too many, and only a few are really useful.
Focus on refactoring your  code to make it as readable as  possible, and as easy
to expand as possible.
Then, whenever you feel like a combination is missing, add support for it.

## ?

Document that `:syn include` sets `b:current_syntax`.

Document that you need to remove `b:current_syntax` after `:syn include`.
Otherwise, if your file contains more  than one embedded language, the next time
you'll  run `:syn  include`,  the contained  groups won't  be  defined, and  the
cluster will contain nothing.

See `~/.vim/plugged/vim-markdown/autoload/markdown.vim` for an example.

## ?

All our markdown syntax code around urls is a mess.
Here are the current existing syntax groups:

markdownAutomaticLink  <http://example.com/>
markdownId
markdownIdDeclaration
markdownIdDelimiter
markdownLink
markdownLinkDelimiter
markdownLinkRefTitle
markdownLinkText
markdownLinkTextDelimiter
markdownUrl
markdownUrlDelimiter  <foo:bar>
markdownUrlTitleDelimiter


Document that there's a difference between:

    <http://example.com/>

And:

    http://example.com/

When you compile a document containing the first text with pandoc, the resulting
pdf  contains an  interactive link  which  you can  open after  pressing `F`  in
zathura; the second text does *not* produce an interactive link.

##
# Reference

[1]: https://vi.stackexchange.com/questions/18318/syntax-regex-optimisations#comment31579_18318
[2]: https://github.com/tpope/vim-markdown/blob/master/syntax/markdown.vim

