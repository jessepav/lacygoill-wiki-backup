# Theory
## What is a
### multi?

A quantifier in Vimspeak.

### piece?

An atom followed by a possible multi.

### concat?

One or several pieces, concatenated.

##
## What is a branch composed of?

One or several concats separated by `\&`.

        concat1 \& concat2 \& ...

### Which of its parts is used to look for a match?

Its last concat.

### On what condition is there a match?

All the previous concats must match at the same place where the last one matches.

### What does it allow me to do?

You can use it to remove  undesirable results, by describing the surroundings of
the match.

##
## What is a pattern composed of?

One or several branches separated by `\|`.

    branch1 \| branch 2 \| ...

### Which of its parts is used to look for a match?

The first (leftmost) matching branch.

##
# Bracket expression
## Are `[` and `]` literal or special outside a bracket expression?

Literal.

### What if they're inside?

`[` is always literal inside a bracket expression.

`]` is literal only at the start of a bracket expression, or if it's backslash-escaped.
Note that the start of a complemented bracket expression is right after `^`.

### Wat's the pattern to describe some random text inside square brackets?

    \[.\{-}]

You don't need to escape the second bracket, because the first one was escaped.
As a result, `]` can't be interpreted  as the end of a bracket expression, since
none has started so far.

###
## How to include a newline in a bracket expression?

Prefix it with `\_`:

    \_[abc]

    ⇔

    [abc\n]

### What if I'm writing a *complemented* bracket expression?

`\_` will still include the newline in the pattern positively.

For example, the  next pattern matches any  character which is not  `a`, `b`, or
`c`, and it also matches the newline.

    \_[^abc]

    ⇔

    [^abc]\|\n

##
# Lookaround
## When should I probably replace `\zs` with `\@<=`?

When the regex you're writing:

   - can have overlapping matches once it's stripped from `\zs`
   - you're interested in all the matches, not just the first one

---

Rationale:

In  `a\zsb`, Vim  matches `ab`,  then  excludes `a`  from the  given match;  but
*internally*, `ab` has been wholly matched; this can make an expected subsequent
match fail.

OTOH, in `a\@<=b`, Vim matches `b`, then it checks whether it's preceded by `a`;
internally, only `b` matches, which is what you expect.

---

Be cautious when you build a regex  from several variables, or define your regex
in one location, then use it in another.
If you  blindly replace  `\@=` with  `\ze`, without looking  at how  exactly the
overall regex is used,  you may end up applying the lookafter  to more text than
you should have; or it may be cancelled by a later `\zs`.

---

Here  are some  examples where  `\zs` causes  an issue,  which can  be fixed  by
replacing it with `\@<=`.

Example 1.

Suppose you have this text:

    abXcd

And you want a regex matching the positions before and after `X`.
This regex will only match after `X` (because alternations are ordered in Vim):

    X\zs\|\zeX

OTOH, this regex matches before and after `X`:

    X\@<=\|\zeX

---

Example 2.

Suppose you want to split `abXcd` into `['ab', 'X', 'cd']` using `split()`:

    ✘
    echo split('abXcd', 'X\zs\|\zeX')
    ['abX', 'cd']~

    ✔
    echo split('abXcd', 'X\@<=\|\zeX')
    ['ab', 'X', 'cd']~

---

Example 3.

A syntax rule may be broken by the usage of `\zs` in another rule:

    " text file
    abXcd

    " broken syntax rules
    :hi link xAb DiffAdd | hi link xCd DiffDelete | syn match xCd /ab.*\zscd/ | syn match xAb /ab/
                                                                       ^^^
                                                                       will cause an issue
    " resulting highlights
    abXcd
    ├┘ ├┘
    │  └ not highlighted ✘
    └ highlighted by `xAb`

    " fixed syntax rules
    :hi link xAb DiffAdd | hi link xCd DiffDelete | syn match xCd /\%(ab.*\)\@<=cd/ | syn match xAb /ab/
                                                                   ^^^    ^^^^^^
                                                                   fixes the issue
    " resulting highlights
    abXcd
    ├┘ ├┘
    │  └ highlighted by `xCd`
    └ highlighted by `xAb`

### Which new pitfall should I be aware of if I do it?

`\@<=` can be significantly  slower than `\zs`, especially if you  use it with a
variable-width subexpression.

---

You can limit the  cost of `\@<=` by limiting how far  Vim should backtrack when
looking for the start of the subexpression.
For example, `\@123<=` limits the backtracking to the 123 earlier bytes.

You should  always use `\@123<=` (and  the negative variant `\@123<!`)  when you
know  the  maximum  byte size  of  the  subexpression  to  which you  apply  the
lookbehind.

### Why is `\zs` affected by this pitfall, but not `\ze`?

I think it's a design choice to get a fast atom.

When `\@<=` is applied to a subexpression, its cost explodes because there is no
way to know in advance where it should start; Vim makes one attempt per previous
character on  the current  line and the  line above; if  there are  123 previous
characters on the current line and the one above, then the cost is multiplied by
123.

I think  that Vim  devs have decided  that it  would be better  for `\zs`  to be
processed  differently  compared  to  `\@<=`;  it  simply  tries  to  match  the
subexpression from  the current position,  and removes  from the match  the text
which  was matched  until `\zs`;  this  way, Vim  doesn't have  to backtrack  in
various earlier  positions and  try to match  from every of  them; it  just stay
where it is and removes some text from the match.

OTOH, with `\ze`, Vim doesn't have to backtrack in various positions and attempt
to match  the subexpression in  each of them;  it just has  to try and  match it
where it currently is when it finds `\ze`; that's why `\ze` is not affected.

In theory, `\zs`  could avoid this pitfall; when processing  the lookbehind, Vim
would need to reverse it (e.g. `a.*b` → `b.*a`), then try to match this reversed
lookbehind *from the current position and backward*.
In that case, the lookbehind would only be matched from one position (instead of
potentially many), the current one.
But  Vim's regex  engine is  not able  to do  that; maybe  reversing a  regex or
matching backward is non-trivial, or too costly...

### More generally, what's the main limitation of `\zs` and `\ze` compared to `\@<=` and `\@=`?

They give less control.

With `\zs` and `\ze`, you can only describe the surroundings of 2 positions (and
only in one direction): the one before  the first character of the match (in the
backward  direction), and  the  one after  the last  character  (in the  forward
direction).
This  is  because  *everything*  that  comes  before/after  is  processed  as  a
lookaround (although, `\zs` and `\ze` stop at an alternation).

With  `\@=` and  `\@<=`, you  can describe  the surroundings  of *any*  position
inside a  match (and  in both  directions), including the  one right  before the
first character, and the one after the last character.
This is because they  allow you to ask for an arbitrary part  of the regex to be
processed as a lookaround, via parentheses.

##
## Why does this regex `.*z\@!` matches the text `abcz`?

`.*` matches `abcz`, and reaches the position right after `z`:

    abcz
        ^

In  that position,  Vim checks  that  there is  no  `z` afterward;  there is  no
character afterward, so `z` can't match, the negative assertion is satisfied and
the overall regex matches `abcz`.

If you want to match only `abc`, use this:

    .*z\@<!

This time, when `.*` matches `abcz`, Vim  checks that there is no `z` before the
position which comes right after `z`; but in that position, there is a `z` right
before; therefore the negative assertion is not satisfied, and the overall match
fails; Vim  can backtrack (thanks  to `*`), and  tries the shorter  match `abc`,
which does satisfy the negative assertion.

##
## When I use `\@<=` or `\@<!`, how far back does the engine search?

Up to the beginning of the previous line.

From `:h /\@<=`:

>     But to  limit the  time needed, only  the line where  what follows  matches is
>     searched, and one line before that (if there is one).
>     This should be sufficient to match most things and not be too slow.

Example:

    $ cat <<'EOF' >/tmp/file
    foo
    bar
    baz
    EOF

    :sp /tmp/file
    /\%(foo\_.*\)\@<=baz
    E486~
    /\%(foo\_.*\)\@<=bar
    [1/1] \%(foo\_.*\)\@<=bar~

Theory: Vim  is  unable  to  distinguish   a  pattern  containing  only  literal
characters from a pattern containing metacharacters.
As a result,  it doesn't try to compute  the size of what you pass  to `\@<=` or
`\@<!`, even if it only contains literal  characters; and it just tries to match
at all possible positions, from the beginning of the previous line.

## When can Vim backtrack more than 123 bytes to process `\@123<=`?

When:

   - the subexpression is multi-line
   - there are less than 123 bytes before the current position on the current line

In that  case, when Vim  reaches the  start of the  current line, it  resets the
number of backtracked bytes to 0.

From `:h \@123<=`:

>     After crossing a line boundary, the limit is relative to the end of the line.
>     Thus the  characters at the  start of  the line with  the match are  not counted
>     (this is just to keep it simple).

---

For example, consider this text file:

    axxxxxxxxx
    xxxxxxxxxb

`\%(a\_.*\)\@10<=b` matches even though there are more than 10 bytes between `a` and `b`.
The match is possible because:

   - the subexpression is multi-line (thanks to `\_.`)
   - there are less than 10 bytes before `b` on the line
   - Vim resets the number of backtracked bytes to 0 when it reaches the start
     of the line

##
## The character `𞹼` weighs 4 bytes.

    $ echo '𞹼' | xxd -p
     f09eb9bc0a~
     ├──────┘├┘
     │       └ ending newline
     └ 4 bytes

### If I search for `\%(𞹼𞹼\)\@5<=a` in the text `𞹼𞹼a`, what will Vim find?

You may think  that Vim won't find  anything because `𞹼𞹼` weighs  8 bytes, while
you limited the search to the 5 previous bytes.
But in practice, Vim *does* find the `a` character.

Theory: The regex engine searches for *characters* not bytes.
So, when you say:

>     don't search back for more than 5 bytes

Vim searches  back for  the least amount  of characters which  weigh 5  bytes or
more; here, it means 2 characters.

### If I search for `\%(𞹼𞹼\)\@4<=a` in the text `𞹼𞹼a`, what will Vim find?

Nothing.

The least amount of characters which weigh 4 bytes or more is 1.
So, Vim searches back for only 1 character, which is insufficient to match `𞹼𞹼`.

##
## How to rewrite `\%(foo\)\@=...` and `\%(foo\)\@<=...` with atoms which don't require parentheses?

Use `\&` and `\zs`:

    \%(foo\)\@=...
    ⇔
    foo\&...
       ^^

    \%(foo\)\@<=...
    ⇔
    foo\zs...
       ^^^

##
# What's the shortest regex to match
## a consonant?

    [^aeiou]\&\a

The regex  matches any alphabetic character  (`\a`), but only if  it's different
than a vowel (`[^aeiou]`).

## any alphabetic character? (even if it has a diacritic sign)

    [[:lower:][:upper:]]

From `:h [:upper:]`:

>     These items  only work  for 8-bit characters,  except [:lower:]  and [:upper:]
>     also work for multi-byte characters when using the new regexp engine.

## a sequence of non-keyword characters?

    \%(\k\@!.\)\+

Useful to simulate `\K\+` (`\K` doesn't exist).

Test the regex against:

    àbc - déf
       ^^^

---

If your Vim includes the patch 8.1.0862, you can also write:

    [^[:keyword:]]\+

The patch introduces these character classes:

   - `[:keyword:]`
   - `[:ident:]`
   - `[:fname:]`

Which can be used to construct the complement of resp. `\k`, `\i`, `\f`.

## the text from the start of the line till the end of `pat` if it matches, or till the end of the line otherwise?

    .*pat\|^.*

Test the regex against:

    a pat b
    ^^^^^^^

    a b
    ^^^

---

Without the  anchor `^`,  on a line  containing `pat`, you  would have  a second
undesired match:

    a pat b
         ^^

---

It works because alternations are *ordered* in Vim.
It means  that the regex engine  uses the *first* matching  alternation; not the
one producing the *longest* match.

## all sequences of several uppercase characters *not* followed by a comma *nor another uppercase character*?

    \%(\u\{2,}\)\@>,\@!
                ^^^

---

Against this text:

    ABC,
    DEF
    GHI,
    JKL

The regex will find `DEF` and `JKL`.

---

This shows how the atom `\@>` can be useful.
Here, without it, we would find `AB`, `DEF`, `GH` and `JKL`.
`\@>` allows us to prevent the backtracking into `\u\{2,}`.

##
## all commas outside a double-quoted string?

    \%(^\%("[^"]*"\|[^"]\)*\)\@<=,
       │                  │
       │                  └ will repeat the strings, and the not-a-strings
       │
       └ necessary; otherwise, the description could start from anywhere,
         which would be too permissive, and all commas would be matched;
         if you don't understand, remove it and remove `\@<=`: look at what's matched

You can test the regex against this line:

    0.12 , 0.15 , "this is a string" , "this is a string, with, many, commas,"

The key  idea, is that  you can  uniquely describe a  comma outside a  string by
expressing  the fact  that it's  preceded by  0 or  more alternation  of strings
(`"[^"]*"`) and not-a-strings (`[^"]`).
This description  won't match  a comma  inside a string,  because there  will be
half-a-string at the end:

    0.12 , 0.15 , "this is a string" , "this is a string, with, many, commas,"
                                       ^^^^^^^^^^^^^^^^^

The underlined text is *not* a full  string so it won't be matched by `"[^"]*"`,
and it's not a not-a-string either, so it won't be matched by `[^"]*` either.

### all commas *inside* a double-quoted string?

    \%(^\%("[^"]*"\|[^"]\)*"[^"]*\)\@<=,
                           ^^^^^^
                           only difference compared to the previous regex:
                           an unterminated string


## all commas outside parentheses?

    \%(^\%(([^()]*)\|[^()]\)*\)\@<=,

Test it against this line:

    0.12 , 0.15 , (inside parentheses) , (inside parentheses, with, many, commas,)

### all commas *inside* parentheses?

    \%(^\%(([^()]*)\|[^()]\)*([^()]*\)\@<=,

##
## a single-quoted string, which may include backslash-escaped single quotes

    '\%(\\.\|[^'\\]\)*'
        ├─┘     ├┘
        │       └ to prevent matching a non-terminated string containing a literal quote
        │         (e.g. '\', '\\\', ...)
        │
        │         Remember the: "no matter what the latter is"?
        │         This `\\` is there to add: "except the final quote".
        │
        └ this is where the main issue is solved:
          if you find a backslash, consume it as well as the next character, no matter what the latter is

Test it against these strings:

    'ab'c
    ^^^^

    'a\'b'c
    ^^^^^^

    'a\\'bc
    ^^^^^

    'a\\\'b'c
    ^^^^^^^^

    'a\\\\'bc
    ^^^^^^^

Notice how  the regex correctly  handles sequences of backslashes;  when looking
for the end  of the string, it only  ignores a quote if it's prefixed  by an odd
number of backslashes (but not if it's prefixed by an even number).

---

You may wonder  why it's necessary to include the  backslash in the complemented
bracket expression:

    '\%(\\.\|[^'\\]\)*'
                ^^

After all, if the regex engine has  to try the second alternation, it means that
`\\.` did  not match; and if  it did not match,  then it means that  there is no
backslash at the current position, right?

Nope.
It's possible  that there  *is* a  backslash at the  current position,  and that
`\\.` *did* match; but  the overall match failed because `.`  matched the end of
the string, which prevented the final `'` to match.

### How to generalize the regex so that it works for double-quoted strings too?

    \(['"]\)\%(\\.\|\1\@![^\\]\)*\1

Test it against these strings:

    'ab'
    'a\'b'
    'a\\'b

    "ab"
    "a\"b"
    "a\\"b

##
## the text between an `A` and the next `C`, with a `B` somewhere in the middle?

    A[^C]*B[^C]*C

Test the regex against:

    AxBxC
    AxxxC

It should match the first line but not the second one.

### Why can't I use `.\{-}`?

You could try. It would give:

    A.\{-}B.\{-}C

Most of the time, it would match the same texts as the previous one.
But not always:

    A C B C
    ^^^^^^^

Here, it would match the whole line, while it should not.
There is no `B` between `A` and the next `C`; just a single space:

    A C B C
     ^

The issue is in the first `.\{-}`.
You need to replace it with `[^C]*`:

    A[^C]*B.\{-}C
     ^^^^^

This seems to  show that, in the  general case, you need  a complemented bracket
expression (`.\{-}` is not enough).

`.\{-}` can be used to express sth like  “the text between the pattern A and the
*next* pattern B”.
But, it can't be used reliably to express sth like “the text between the pattern
A and the next pattern B *with* a pattern C in the middle”.

### How to adapt the regex when C is a multi-character text, like `PAT`?

Replace `[^C]*` with `\%(\%(PAT\)\@!.\)*`

    A\%(\%(PAT\)\@!.\)*B\%(\%(PAT\)\@!.\)*PAT

Test the regex against this text:

    AxBxPAT
    AxxxPAT

It should match the first line but not the second one.

###
### What if B is `\%#`?

The regex works, but  you probably want an additional branch  to handle the case
where the cursor is right before `A`.

    A[^C]*\%#[^C]*C\|\%#A[^C]*C
                   ^^^^^^^^^^^^

Indeed, when you see  your cursor *on* `A` in normal  mode, you'll probably want
your regex to match.
But for the regex engine, your cursor is not on `A`, but *right before* (so it's
not inside "from `A` up to the next `C`", but right before).

### What if A = C?

It  depends  on whether  you  allow  matches  in-between two  consecutive  texts
surrounded by pairs of As.

If you do, then use this regex:

    \%(A[^A]*B\)\@=A[^A]*A
    ├─────────────┘├─────┘
    │              └ text surrounded by a pair of As
    └ B must be in the middle

If you don't:

    \%(^\%(A[^A]*A\|[^A]\)*\)\@<=A[^A]*B[^A]*A
           ├─────┘  ├──┘  │      ├───────────┘
           │        │     │      └ a text surrounded by a pair of As with B in the middle
           │        │     └ there can be several of them
           │        └ there can be a character outside a text surrounded by a pair of As before
           └ there can be a text surrounded by a pair of As before

Test the regexes against this text:

    AxA   AxBxA
    AxA B AxA

---

You may  be used  to a  lookahead written after  a matched  character, and  to a
lookbehind written before a matched character.
So, you  may be  surprised that in  the second regex,  the lookahead  is written
after *nothing*, and the lookbehind is written before *nothing*.

Don't be surprised.
A lookaround is not *applied to* the previous or next matched character.
It's  *searched for*  at  the position  reached  by the  regex  engine when  the
lookaround is processed.

#### Is there an alternative?

You could replace the last regex with this one:

    \%(.*B\)\@=\%(A[^A]*A\)\@>\%(B.*\)\@<=
    ├─────────┘├─────────────┘├──────────┘
    │          │              └ B must be before
    │          └ text surrounded by a pair of As
    └ B must be after

However, it only works as expected when there is one B per line, not several.
For example, in this text:

    AxA AxBxA B AxA AxBxA
                ^^^

It wrongly matches the second `AxA`.

Besides, I don't understand how the atomic group prevents a match in-between two
consecutive texts surrounded by pairs of As.

Without it, the regex becomes:

    \%(.*B\)\@=A[^A]*A\%(B.*\)\@<=

And this new regex finds a match here:

    AxxA B AxxA
       ^^^^^

`\@>` prevents the regex engine from backtracking, but I don't understand how it
has any effect here.
It can't  give up any character  inside `A B A`  anyway (if it did,  it couldn't
match the second A anymore), so there is no submatch which `\@>` can prevent.

It seems to be due to a combination of:

   - the new NFA engine being used
   - a variable-width lookafter
   - an atomic group

Indeed,  these regexes  do match  `A B A`,  which  is more  compatible with  my
understanding of regexes:

    " no new engine
    \%#=1\%(.*B\)\@=\%(A[^A]*A\)\@>\%(B.*\)\@<=

    " no variable-width lookafter
    \%#=2\%(..B\)\@=\%(A[^A]*A\)\@>\%(B.*\)\@<=

    " no atomic group
    \%#=2\%(.*B\)\@=A[^A]*A\%(B.*\)\@<=

The regex probably works only because of an implementation detail.
The implementation could change in the future, therefore the regex is unreliable.
Don't use it.

---

Here's another example where the new engine processes an atomic group in a weird
way.

Let's assume you want `bar` in `[foo](bar)` when it's under the cursor.
Here's a one possible regex:

    \%(.*\%#\)\@=\%(\[.\{-}\](\zs.\{-}\ze)\)\@>\%(\%#.*\)\@<=

Which can be tested against this text:

    one [two](three) (four) [five](six) seven
                                    ^
                                    cursor here

With the old engine, the match is `six`.

With the new engine, the match is `[five](six)`, while I would expect just `six`
(thanks to `\zs` and  `\ze`); it's as if the new engine  ignored `\zs` and `\ze`
inside the atomic group.

##
## the quoted string under the cursor?

    \%(.*\%#\)\@=\%('[^']*'\)\@>\%(\%#.\+\)\@<=
    ├───────────┘├─────────────┘├─────────────┘
    │            │              └ the cursor must be before the closing quote
    │            └ two consecutive quotes
    └ the cursor must be after the opening quote

Test the regex against this text:

    a 'string' and 'another one' !

---

The lookahead `\%(.*\%#\)\@=`  is applied to the position right  before the next
matched character (i.e. the opening quote).
It expresses that you want the cursor  to be somewhere after the position before
the opening quote.

And the lookbehind `\%(\%#.\+\)\@<=` is applied  to the position right after the
previous matched character (i.e. the closing quote).
It expresses that you want the cursor to be somewhere after the closing quote.

### Why the `+` quantifier in the second lookaround?

To prevent a match when the cursor is right after the closing quote.

Indeed, between  the cursor position  and the  position right after  the closing
quote, there must be at least one character: the closing quote.

If you use `*` instead, then you  allow 0 characters between the cursor position
and the position  right after the closing quote; which  happens when your cursor
is right after the closing quote.

### Why the atomic group?

To prevent a match when you're outside a string.

For example, when your cursor is on the `n` of `and`:

    a 'string' and 'another one' !
                ^

The regex – without `\@>` – matches `' and '` in this position:

    a 'string' and 'another one' !
             ^^^^^^^

---

It's also  necessary to prevent a  match when you're  on the opening quote  of a
string which is not the first on the line.

For example, on this position:

    a 'string' and 'another one' !
                   ^

The regex – without `\@>` – would match `' and '`:

    a 'string' and 'another one' !
             ^^^^^^^

####
# Miscellaneous
## When Vim's regex engine processes 2 alternations, both matching the text, which one is used to produce a match?

The first one.

Alternations in Vim's regex engine are  neither lazy (the shortest matches), nor
greedy (the longest matches), it's *ordered* (the first matches).

That's why this regex:

    tour\|to\|tournament

matches `tour` in the text:

    three tournaments won
          ^^^^

If it was lazy, it would match `to`, and if it was greedy, it would match `tournament`.

---

This is not the case of all regex engines.
In some of them, alternations are greedy.

For more info, have a look  at the book “Mastering Regular Expressions”, chapter
4, section “Is Alternation Greedy?” (page 198 of the pdf).

###
## My regex matches a multi-line text.
### Which text does Vim ignore when looking for the start of the next match?

Only the first line of the previous match.

For example, if your text file contains only:

    a
    a
    b

and your regex is:

    a\_.*b

Vim finds two matches:  from the first `a` up to the `b`,  *and* from the second
`a` up to the `b`.

This is specific to Vim; e.g. PCRE and Python would only match from the first `a`:
<https://regex101.com/r/RQbIQc/1>

###
## Why should I prefer the `=` quantfier instead of its synonym `?`?

If you use  your regex in a  backward search, you'll have to  double escape `?`,
which is awkward.

For example, it's simpler to read:

        ?fooz\=bar

than:

        ?fooz\\?bar

## Why should I use a backward search (`?` instead of `/`) to test a regex containing a slash?

To avoid having to escape the slash.

For example, it's simpler to read:

    ?foo/bar

than:

    /foo\/bar

###
## What kind of atom is `\@>`?

An atomic group.

It prevents the regex engine from backtracking into anything inside.

---

An  atomic group  is a  group  that –  when the  regex  engine exits  from it  –
automatically throws  away all backtracking  positions remembered by  any tokens
inside the group.

See: <https://www.regular-expressions.info/atomic.html>

### What is its purpose?

It prevents the engine from backtracking after a subexpression has been matched.

For example,  if your pattern  is `\%(a.\{-}b\)\@>c`, after  matching `a.\{-}b`,
the regex may still fail to match `c`.
If that happens, the engine could backtrack into `a.\{-}b` thanks to `\{-}`; but
`\@>` prevents the engine from doing this.

In practice, it's used  to optimize a regex, or it can  be necessary to describe
the text you're interested in.

### Where can I find more info about it?

   - `:h /\@>`
   - <https://www.regular-expressions.info/atomic.html>
   - <http://perldoc.perl.org/perlre.html#extended-patterns>

##
# Issues
## What is the first thing I should do when my regex doesn't produce the expected matches?

Use it as the pattern of a substitution command with a confirmation flag:

    :%s///gc
       ├┘
       └ use last pattern (assumes that you've just searched your regex in a `/` command)

When `:s` asks for your confirmation, press `n` to leave the text unchanged.
Before each  confirmation request, you can  see the matched text  highlighted by
`IncSearch`.

---

Rationale:

The text highlighted by `Search` may not be the one you expect.
And you may infer from this highlighting that your regex is wrong.
It's not necessarily the case; your regex could still be correct.

As an example, consider this regex:

    a\_.*b

And this text file:

    a
    a
    b

If you search for  the regex in a `/` command, *all* the  text is highlighted by
`Search` (*and* by `IncSearch` right before pressing Enter).
This could give you the wrong impression that there is only one match.
But in reality,  there are two matches: from  the first `a` up to  `b`, and from
the second `a` up to `b`.

---

As another example, consider this regex:

    ^###\n.*\n###

And this file:

    ###
    foo
    ###
    bar
    ###
    baz
    ###

If you look at the `Search` highlighting,  it really looks like there are only 2
matches; this one:

    ###
    foo
    ###

and this one:

    ###
    baz
    ###

But in reality, there's a third match in the middle:

    ###
    bar
    ###

---

As a final example, consider this regex:

    \(.*\%#\)\@=`[^`]*`\(\%#.*\)\@<=

And this text, while your cursor is on `four`:

    one `two` three `four` five
            ^^^^^^^^
            highlighted

But the real text matched by the regex is not the one highlighted.
You can see it by running `:%s///gc`:

    one `two` three `four` five
                    ^^^^^^

The `Search` highlighting is probably  unreliable because right after the search
command,  the cursor  is moved,  and  thus the  position expressed  by `\%#`  is
altered.

### Ok, I did it.  Doesn't help.  What now?

Prefix your regex with `\%#=1`.
This will force Vim to use its old regex engine, which "supports everything".
From `:h two-engines`:

>     1. An old, backtracking engine that **supports everything**.

If your  regex now works as  expected, it means that  Vim was using the  new NFA
engine, and you were using some feature not supported by the latter.

Otherwise, try to prefix it with `\%#=2` to force Vim to use the new NFA engine.
If it now works as expected, it means that Vim was using the old engine, and you
were using some feature not supported by the latter.

Note that `\%#=1` and `\%#=2` must be written at *the very beginning* of the regex.
Even before sth like `\m` or `\v`.

---

Finally, if the  regex still does not  work as expected, simplify it  as much as
possible, as well as the testing text.
Then, try to translate the result in PCRE, and test it on [regex101.com][1].

If it produces the expected match(es), it probably means that there is a bug in Vim.
Have a look at `:h todo` and Vim's issue tracker; maybe it's a known bug.

Otherwise, it probably  means that you're missing some knowledge;  in that case,
regex101.com can help you by providing an explanation of the PCRE regex.

##
## I wrote some code using a regex.  It works in most buffers.  But in one of them, it works differently!

Make sure to temporarily reset the local value of `'isk'` to its global value:

    let isk_save = &l:isk
    try
        set isk&vim
        " use your regex
    finally
        let &l:isk = isk_save
    endtry

Do the same for `'isf'`, `'isi'` and `'isp'` if your regex includes `\f`, `\i`, `\p`.

---

MWE:

    com Test call Func()
    fu Func() abort
        let func_name = 'function! Some_name() abort'
        echo matchstr(func_name, '^\k\+!\=\s\+\zs\k\+')
    endfu

    :Test
    Some_name~
      in most buffers (✔ expected)~

    Some_name()~
      in a help buffer (✘ UNexpected)~


This happens because in a help buffer, `'isk'` contains this value:

    !-~

It includes the parentheses:

    :echo map(range(char2nr('!'), char2nr('~')), {_,v -> nr2char(v)})
    ['!', ..., '(', ')' ..., '~']~
                ^    ^
                ✘    ✘

Which makes the previous regex fail to match the name of the function.
The parentheses will be, wrongly, included inside the match.

---

Bottom line:

A command  whose purpose is to  operate on the  text of the *current*  buffer is
fine, because it needs to take the buffer settings into account.

But if  the command  has to  operate on  some text  which is  *not* tied  to any
buffer, and your regex includes one of these atoms:

    \<
    \>
    \f
    \i
    \k
    \p

The regex will be affected by the buffer-local values of some options:

   - `'isfname'`
   - `'isident'`
   - `'iskeyword'`
   - `'isprint'`

Which may have unexpected results.

## What's one pitfall of using the complement of a bracket expression?

Is your complement preceded by an atom followed by a quantifier?
If so, make sure your bracket expression includes this atom, or use `\@>` on the
previous atom.

---

Example:

you have this text:

    aaa   xyz
    aaa   bxyz

You want to match the next sequence of non whitespace after `aaa` on the first line.
So you try this regex:

    a\+\s\+\zs\S\+

It matches `xyz` on the first line (✔), but also on the second line (✘).
So you try this regex:

    a\+\s\+\zs[^b]\S\+

Now it matches `xyz` on the first line (✔), but also `bxyz` on the second line (✘).
This is because the engine backtracked:
`\s\+` gave back one space, and `[^b]` matched it.
The solution is to include a whitespace in the complement of your collection:

    a\+\s\+\zs[^b \t]\S\+

You could also use `\@>` to prevent the regex engine from backtracking into `\s\+`:

    a\+\%(\s\+\)\@>\zs[^b]\S\+

##
## I'm writing a script.  `\%#` doesn't work!

Replace it with `\%123c`, where `123` stands for the output of `col('.')`.

For example, if your pattern is:

    let pat = '\k*\%#\k*'

You can rewrite it like so:

    let col = col('.')
    let pat = '\k*\%'..col..'c\k*'

---

`\%#` works in a `/` command, and in a call to `search()`.
In both cases, Vim searches directly in the current buffer.

But it doesn't work in sth like:

    let line = getline('.')
    let str = matchstr(line, '\k*\%#\k*')
                                 ^^^

because `matchstr()`  doesn't search directly  in the  current buffer, but  on a
copy of the current line provided by `getline('.')`.
In this copy, the cursor position is lost.

##
##
##
# Lookahead / concats

`@<!` peut être lent; dans ce cas, préférer `@123<!`.

Les positive /  negative lookbehind peuvent considérablement  ralentir le moteur
de regex.
Qd on cherche  un pattern contenant l'un  de ces multi, et que  la recherche est
trop lente (+ consommation  cpu en hausse), il faut utiliser  une version de ces
multi limitée à un nb restreint d'octets:

    \%(...\)\@12<=
    \%(...\)\@34<!


    \v((foobar)@!.)+&<\k{3,}>

            N'importe quel mot de plus de plus de 3 caractères, différent de 'foobar'.


    \v(foobar)@!.
    \v(foobar)@<!.

            n'importe quel caractère à condition que ce ne soit pas le `f` d'un `foobar`
            n'importe quel caractère à condition qu'il ne soit pas précédé de `foobar`

                                               NOTE:

            Il est probable que dans la 1e syntaxe, `@!` soit appliqué au “début du match“.
            Un peu comme si le “début du match“ était une ancre.
            IOW, le moteur de regex vérifie, avant chaque tentative de matcher le pattern,
            que `foobar` n'est pas là.


    \vif (.*then)@!.*
    \vif ((then)@!.)*$

            depuis un if jusqu'à la fin d'une ligne, sans que then se trouve qq part après if

            La 2e syntaxe pourrait se lire comme ceci:

                    ((then)@!.)*       (then)@!.(then)@!.(then)@!.    ...

            ... et    .(then)@!    matche un caractère à condition qu'il ne soit pas suivi d'un then.

            @! ne fait pas reculer le moteur après qu'il ait matché le dot.
            En réalité, il lui demande de vérifier qu'il n'y a pas de then APRÈS le match en cours.
            On pourrait sans doute aussi utiliser    (then)@<!.    un caractère qui n'est pas précédé de then.

            L'ancre $ est obligatoire dans la 2e syntaxe, autrement on matche du if jusqu'à un éventuel
            then (then exclu).


    \vfoo((bar)@!\_.)*qux

            un texte compris entre foo et qux, sans que bar ne soit présent entre les 2

            Si on inversait (bar)@! et \_. comme ceci:

                    \vfoo(\_.(bar)@!)*qux

            ... on ne s'assurerait pas que bar ne suit pas directement foo.
            Pex, on risquerait de matcher 'foobar hello qux'.


    \v.*foo&^.*bar

            n'importe quelle ligne contenant 'bar' mais seulement si elle contient 'foo'

            IOW, match n'importe quelle ligne contenant à la fois 'foo' et 'bar' dans n'importe quel ordre.

            Le & demande à Vim de vérifier qu'il peut matcher .*foo depuis le même début de ligne
            à partir duquel il a déjà réussi à matcher .*bar.

            Attention, le texte matché est .*bar. Il peut contenir 'foo' ou pas.
            En effet, il se peut qu'il ne contienne pas 'foo' si ce dernier se trouve après 'bar'.

            .*foo n'est présent que pour vérifier que le match .*bar est possible ou non, comme une ancre.
            Il n'ajoute / ne retire rien au match.


                                               NOTE:

            On pourrait aussi utiliser des branches pour obtenir le même résultat:

                    .*foo\zs.*bar\|.*bar\ze.*foo

            Mais c'est moins lisible, et ça deviendrait de plus en plus complexe si on ajoutait
            d'autres concats:

                    \v.*foo&.*bar&.*baz


                                               NOTE:

            On pourrait aussi utiliser un lookbehind (`%()@=`).

                    \v^%(.*foo)@=.*bar    ✔✔    très rapide
                    \v%(^.*foo)@=.*bar    ✔     rapide
                    \v%(.*foo)@=.*bar     ✘✘    extrêmement lent

            Il ne faut pas en déduire qu'un concat peut tjrs être remplacé par un lookaround.
            Il n'y a pas d'équivalence entre les 2 items.
            Un concat et un lookaround permettent d'ajouter une description concernant des choses
            différentes:

                    - ce qui se trouve à l'intérieur du match via un concat
                    - "                  l'extérieur "               lookaround

            Dans le cas présent, on peut utiliser un lookbehind à la place du concat, uniquement
            car la description supplémentaire dont on a besoin, concerne du texte situé à l'extérieur
            du match. Quel texte?
            Le début de la ligne où bar se trouve; on veut qu'il soit le début d'une ligne contenant foo.


                                               NOTE:

            Il semble qu'un lookbehind soit plus rapide qu'un concat.
            En particulier qd il s'agit d'un negative lookbehind. À vérifier.

                    \v^%(\s*".*)@=.*\zsfoo      ✔✔ très rapide
                    \v\s*".*&^.*\zsfoo          ✔  rapide

                    \v^%(\s*".*)@!.*\zsfoo      ? plus ou moins rapide?
                    \v^%(\s*".*)@!&^.*\zsfoo    ? lent? moins rapide?


                                               NOTE:

            On pourrait se passer de l'ancre `^` ou la déplacer dans l'autre concat, mais ça aurait
            un impact sur la rapidité du moteur de regex pour traiter le pattern:

                    \v.*foo&^.*bar    ✔✔    très rapide
                    \v.*^foo&.*bar    ✔     rapide
                    \v.*foo&.*bar     ✘✘    extrêmement lent

            Pour rappel, afin de mesurer la rapidité du moteur de regex à traiter un pattern:

                    :{big number}Time /pattern

# Quantificateurs / Ancres

Quelques quantificateurs (:h /multi) :

    ┌───────────────┬────────────────────────────────┐
    │ *   ou {-}    │ 0 ou +  (greedy vs non-greedy) │
    ├───────────────┼────────────────────────────────┤
    │ +   ou {-1,}  │ 1 ou +  (")                    │
    ├───────────────┼────────────────────────────────┤
    │ ? = ou {-,1}  │ 0 ou 1  (")                    │
    ├───────────────┼────────────────────────────────┤
    │ {n,m}         │ n à m                          │
    ├───────────────┼────────────────────────────────┤
    │ {n}           │ exactement n                   │
    ├───────────────┼────────────────────────────────┤
    │ {n,} ou {-n,} │ n ou + (greedy vs non-greedy)  │
    ├───────────────┼────────────────────────────────┤
    │ {,m}          │ de 0 jusqu'à m                 │
    └───────────────┴────────────────────────────────┘

Quelques ancres/atomes ordinaires de largeur nulle (:h /zero-width) :


    ^
    $

            Début/Fin de ligne qd il se trouve:

                - au début/à la fin du pattern
                - "                 d'une branche ( juste après un \| )
                - "                 d'un groupe ( juste après un \( / avant un \) )
                - juste après/avant un \n

            Autrement, matche le caractère ^/$.

            Il n'ajoute rien au pattern, il dit simplement que le précédent/prochain caractère doit
            être un newline.


    \_^
    \_$

            Début / Fin de ligne.
            Utilisable n'importe où au sein du pattern (`^ $` y seraient parfois interprétés littéralement).

            Cette ancre signifie que le précédent / prochain caractère est un newline.
            Utile après/avant un \_{class}{multi} pour signifier que le dernier/1er caractère doit
            être un newline.

            Ex:
                    \v\_.+\_^

            Ici, on répète un caractère qcq (y compris un newline grâce à \_.), mais la dernière répétition
            doit être un newline (à cause de \_^).

                    \v\_$\_s+

            Ici, on répète un whitespace ou un newline, mais la première répétition doit être un
            newline (à cause de \_$).


    \v(.{-}\zsfoo){3}

            matche la 3e occurrence de foo sur la ligne
            Ceci montre que \zs peut être utilisé plusieurs fois, et que dans ce cas seul le dernier compte.
            En effet, le dernier pattern équivaut à:    \v.{-}\zsfoo.{-}\zsfoo.{-}\zsfoo


    \%V

            Le caractère qui suit est dans la sélection visuelle.

            Pour  décrire  un  pattern  limité  à  l'intérieur  d'une  sélection
            visuelle, il faut l'encadrer avec 2 atomes %V:

                    \v%Vpattern%V


            Exemple:

                    ┌ colonne sélectionnée
                    ├───────────┐
                    foo 1 bar foo 2 bar
                    foo 1 bar foo 2 bar
                    foo 1 bar foo 2 bar
                    ├───────┘
                    └ texte recherché
                      pattern à utiliser:    \v%Vfoo.*bar%V


                                               NOTE:

            Si la fin du pattern coincide avec la fin de la sélection, il faut faire reculer le 2e %V :

                    \v%Vpatter%Vn

            Il se peut qu'on doive faire la même chose si la fin du pattern utilise un quantificateur.


                                               NOTE:

            On peut utiliser `@!` pour inverser le sens de `%V`:

                    \v%Vpattern%V@!

            Exemple:

                     ┌ colonne sélectionnée
                     ├──┐
                    a1   a       a   1a
                    b12  b   →   b  12b
                    c123 c   ^   c 123c
                    d1234d   │   d1234d
                             │
                             │
                            *s/\v%V(.{-})(\s*)%V@!/\2\1/
                                              ├──┘
                                              └ Le caractère qui suit ne doit pas être dans la sélection.
                                                Ne fonctionnerait sans doute pas si la fin
                                                du pattern utilisait un quantifcateur non-greedy.

                                                Sans `@!`, le pattern pourrait matcher un texte vide,
                                                présent devant chaque caractère de la sélection.


                    a1   a           a   1a
                    b12   b     →    b  12 b
                    c123   c    ^    c 123  c
                    d1234   d   │    d1234   d
                                │
                                │
                                *s/\v%V(\S*)(\s*)%V(.)/\=submatch(3) =~ '\s' ? submatch(2).submatch(3).submatch(1) : submatch(1).submatch(3)/

                                Cette substitution gère aussi le cas précédent.


    \%>'m
    \%'m
    \%<'m

            Après la marque m, là où se trouve la marque m, avant la marque m.


                                               NOTE:

            Pattern utile pour capturer une sélection visuelle characterwise ou linewise:

                    \%'<\_.*\%<'>..

            Remarque 1:

                    \%'<\_.*\%'>.     ✘

            Ne fonctionne pas si la sélection est linewise.
            Le pb vient sans doute du fait que dans ce cas la colonne de la marque `'>` est infinie.
            Confirmée par:

                    :echo getpos("'>")
                    2147483647~

            Cette position est fausse, et Vim ne trouvera jamais autant de caractères sur une ligne.

            Une solution consiste à utiliser l'ancre:         \%<'>

            Cette dernière matche juste avant la marque `'>`.
            Pour une raison que j'ignore, ça résoud le pb.

            Remarque 2:
            Ne cherche pas à réécrire le pattern en mode very-magic, j'ai pas réussi.


    \v%>12l
    \v%12l
    \v%<12l

            Le prochain caractère est:
            après la ligne 12 (12 exclue), sur la ligne 12, avant la ligne 12 (12 exclue)

            \%>12l et \%<12l signifient que la ligne du caractère suivant doit être strictement
            supérieure / inférieure à 12.


    \v%>34v
    \v%34v
    \v%<34v

            Le prochain caractère est:

                    après la 34e colonne de l'écran (34e colonne exclue)
                    sur la 34e colonne de l'écran
                    avant la 34e colonne de l'écran (34e colonne exclue)

            \%>34v et  \%<34v signifient que  l'index du caractère  suivant doit
            être strictement supérieur / inférieur à 34.

                                               NOTE:

            Quelle différence entre \%>34v. et \%34v. ?
            \%>34v. matche n'importe quelle colonne à partir de la 35e
            \%34v. matche la 34e colonne


                                     NOTE:

            Try to avoid `\%v` as much as possible, and use `\%c` instead.
            How `\%123v` is interpreted may be influenced by some options.
            See `./vimL.md` for more info.

            Although, I guess  it's ok to use `\%v` when  you're sure your lines
            are NOT wrapped.


    \v%>56c
    \v%56c
    \v%<56c

            Le 1er octet du prochain caractère est:
            après le 56e (56 exclu), le 56e, avant le 56e (56 exclu)

            \%>56c et \%<56c signifient que l'index de l'octet suivant doit être
            strictement supérieur / inférieur à 56.

                                     NOTE:

            `\%123c` commence à indexer à partir de 1, et non de 0, comme `col()`.

                    /\%0c
                    E486: Pattern not found: \%0c~


    \%42v.
    \%42c.

            Le caractère occupant la 42e colonne sur la ligne.
            Le caractère dont le 1er octet est le 42e sur la ligne.

    .\%42v
    .\%42c

            Le caractère occupant la 41e colonne sur la ligne.
            Le caractère dont le dernier octet est le 41e sur la ligne.


    \v%2l%5v.

            Caractère occupant la 5e colonne sur la 2e ligne.


    \v%10l.|%20l.

            Un caractère sur la ligne 10 ou 20.


    \v%>4l%<11lfoo

            `foo` entre les lignes 5 et 10

                                               NOTE:

            \v%>4l%<11l signifie simplement que le prochain caractère ('f') doit être entre la ligne 5 et 10.
            Le reste du pattern peut être sur n'importe quelle ligne.
            Pex, si on a un foo sur la ligne 10 et un bar sur la ligne 11, le pattern:

                    \v%>4l%<11lfoo\nbar

            ... matchera ces 2 lignes, bien que 'bar' soit sur la ligne 11.


    \v%>43v.%<46v

            44e caractère.

            \%>43v demande à ce que le caractère suivant ait un index >43
            \%<46v demande à ce que le caractère suivant ait un index <46, ce qui impose au caractère
            précédent d'avoir un index <45

            Le 44e caractère est le seul caractère remplissant ces 2 conditions.


    \v%>43v%<46v.

            Caractères 44 et 45

# Atomes

Une classe de caractères est une séquence d'échappement spéciale représentant un
ensemble de caractères ayant un point commun (lettres, chiffres...).

Un atome est un caractère ordinaire, ou une classe de caractères, ou une ancre.
It's something that you can't break in two parts without changing its meaning.
For example, you  can break `ab` in  two parts, because looking for  `ab` is the
same as looking for `a` then for `b`.
But you can't break `\a` in two parts,  because looking for `\a` is NOT the same
as looking for `\` then `a`.

Quelques classes (:h /character-classes) :

    . ou \_.        n'importe quel caractère (sauf newline pour le 1er, y compris newline pour le 2e)

                                               NOTE:

                    Dans une chaîne passée à `matchstr()`, `.` représente n'importe quel caractère,
                    y compris un newline. `.` et `\_.` sont alors équivalents.

    \a \A           (non-)alphabet [A-Za-z]
    \b              backspace
    \d \D           (non-)chiffre
    \h \H           (non-)head of word character [a-zA-Z_]
    \l \L           (non-)lettre minuscule [a-z]
    \u \U           (non-)lettre majuscule [A-Z]

                                               NOTE:

    \u \U  \l \L n'ont  pas la même  signification suivant qu'ils  sont utilisés
    dans un pattern ou dans une chaîne de remplacement.
    Dans un pattern, il s'agit d'un des atomes qu'on vient de voir.
    Dans une  chaîne de remplacement, ils  modifient la casse d'un  ou plusieurs
    caractères développés à partir de `\0`, `\1`, ..., `\9`, `&`, `~`.


    \_x

            classe de caractères \x (ex: \a, \d, \s) en incluant le newline

    \_[...]    [...\n]

            collection de caractères incluant le newline

    \(\)

            transforme le pattern à l'intérieur en sous-expression à laquelle on peut:

                - appliquer un multi
                - ajouter une ancre avant ou après
                - se référer plus tard (\0, \1, ... \9; submatch(0), submatch(1), ...)

                                               NOTE:

            Il  semble  que  les  patterns  entourés  de  parenthèses  dans  des
            negative/positive lookahead/lookbehind, ne sont pas capturés.
            Raison pour laquelle, si on fait  un \=submatch(0) dans la chaîne de
            remplacement, on obtient bien tjrs le match voulu.


    [...]

            Ensemble de caractères (collection).
            N'importe quel caractère présent à l'intérieur des [] comme si on les séparait par des OU.
            Principe de construction des expressions brackets.

            :h /collection pour + d'infos.

                                               NOTE:

            On peut y inclure des caractères spéciaux tq \n, \r, \t, ainsi que des classes
            utilisant la syntaxe `[:{word}:]`.
            Mais on ne peut pas y inclure les autres tq \s ou \d (:h /character-classes).


    [^...]

            N'importe quel caractère sauf ceux à l'intérieur de la collection.
            Inversion de collection.

                                               NOTE:

            Dans une collection, le positionnement des caractères `-` et `^` a un sens.

                    - au début de la collection     ^ inverse cette dernière
                    - au milieu ou à la fin         ^ est l'accent circonflexe
                    - entre 2 lettres ou chiffres   - décrit une rangée de caractères
                    - ailleurs                      - décrit un tiret

            Pour être sûr qu'un tiret soit interprété littéralement dans une collection,
            il vaut mieux le placer au début.

            Si on veut utiliser `^` et `-` chacun avec son sens spécial, il vaut mieux
            écrire:

                    [^-...]    n'importe quel caractère sauf un tiret et d'autres caractères ...


    [abc\u00a0]

            Collection contenant les caractères `a`, `b`, `c` et l'espace insécable.

            Illustre qu'au sein d'une collection, on peut représenter un caractère via son point
            de code décimal/octal/hexa.

                                               NOTE:

            Dans ce cas il ne faut pas utiliser le caractère % comme on le ferait si on était
            en-dehors d'une collection (mais tjrs au sein d'un pattern).

            En effet, si on écrivait [\%u00a0], Vim chercherait les caractères \ % u 0 a.

            Voici un résumé expliquant comment représenter l'espace insécable suivant le contexte:

                    - "\u00a0"    dans une chaîne non littérale

                    - [\u00a0]    dans une collection au sein d'un pattern

                    - \%u00a0     partout ailleurs dans un pattern

            Il n'y a que dans un pattern que `%` est nécessaire.
            Il sert à distinguer certaines classes (\d \o \x \u \U) de caractères définis par
            leur point de code.

            Voici quelques patterns similaires mais dont le sens est très différent
            suivant qu'on utilise ou non `%`:

                    \u20AC                            \%u20AC
                    lettre majuscule                  caractère dont le point de code en hexa est 20AC
                    suivie de '20AC'                  €

                    \U10000                           \%U10000
                    lettre non-majuscule              caractère dont le point de code en hexa est 10000
                    suivie de '10000'                 𐀀

                    \x2a                              \%x2a
                    chiffre en base 16                caractère dont le point de code en hexa est 2a
                    suivi de '2a'                     *

                    \d123                             \%d123
                    chiffre décimal                   caractère dont le point de code en décimal est 123
                    suivi de '123'                    {

                    \o173                             \%o173
                    chiffre octal                     caractère dont le point de code en octal est 173
                    suivi de '173'                    {

            Mais une collection ne peut contenir que des caractères, pas de classes tq \u ou \d.
            Ces notations sont donc libres et peuvent être utilisées pour représenter un caractère
            d'un point de code donné. Raison pour laquelle on n'utilise pas `%` dans une collection.

            De la même façon, seul le moteur de regex interprète:

                    \d \o \x \u \U

            ... comme une classe.
            Donc dans une chaîne qui n'est pas passée au moteur de regex, ces notations sont libres.
            On peut donc les utiliser, sans `%`, pour représenter un caractère à partir de son point
            de code en décimal ou en octal.


                                               NOTE:

            Un caractère multi-octets peut provoquer une erreur au sein d'une commande de substitution,
            et peut-être au sein d'autres commandes.
            Dans un script, il vaut mieux utiliser la notation utilisant son point de code.


    \%u00a0

            matche le caractère dont le point de code est 00a0, un no-break space (&nbsp;)

            Plus généralement, on peut représenter un caractère à partir de son point de code via les atomes:

                    - \%d    valeur en décimal    autant de chiffres que nécessaire

                    - \%o    valeur en octal      jusqu'à 3 chiffres, le max étant 377
                                                  377₈ = 255₁₀

                    - \%x    valeur en hexa       jusqu'à 2 chiffres
                    - \%u    "                            4 chiffres
                    - \%U    "                            8 chiffres

            Attention, il vaut mieux fournir un max de chiffres, quitte à ajouter des leading 0.
            Autrement, les caractères suivants pourraient être interprétés comme faisant partie du
            point de code.

            Par exemple, si on cherche un bang à partir de son point de code (\%u0021) suivi des
            chiffres 0 et 3:

                    \%u002103    ✔
                    \%u2103      ✘    car \%u2103 ~= ℃

            Ou alors, il faut que les caractères qui suivent ne soient pas des chiffres utilisés
            en base 8, 10 ou 16, en fonction de la base dans laquelle est écrite le point de code.


    [[:cntrl:]]

            La classe des caractères de contrôle.

            Techniquement `[:cntrl:]` est un atome particulier, car il ne peut être utilisé qu'au
            sein d'une expression bracket.

            En effet, en-dehors de crochets, `[:cntrl:]` serait interprété comme un des caractères
            suivants:        `:`, `c`, `n`, `t`, `r`, `l`

            Il existe d'autres classes similaires:

                        - [:blank:]        espace ou tab horizontal
                        - [:cntrl:]        caractères de contrôle (inclue un tab, bizarre ...)
                        - [:digit:]        \d
                        - [:graph:]        caractères ascii sauf espace
                        - [:lower:]        \l
                        - [:print:]        caractères affichables
                        - [:punct:]        caractères de ponctuation
                        - [:space:]        whitespace (dépend de ce que Vim considère comme un whitespace)
                        - [:upper:]        \u
                        - [:xdigit:]       \x

            Elles sont similaires par leur forme ([:{word}:]), et par leur utilisation (uniquement
            au sein d'une collection).

            Ce sont les seules classes pouvant être incluses au sein d'une collection.


    [-./[:alnum:]_~]\+

            Matche un nom de fichier unix.

            En effet, un nom de fichier unix peut contenir un:

                    - tiret
                    - point
                    - slash
                    - caractère alphanumérique
                    - underscore
                    - tilde

            [:alnum:] est la classe des caractères alphanumériques.

            Illustre qu'un atome spécial tq [:alnum:], [:cntrl:], ... peut être accompagné
            d'autres caractères au sein d'une collection.


    [[=a=]]

            ensemble des caractères voisins de 'a' (aàâ)

            Techniquement, il  s'agit d'une  expression de classe  de caractères
            appelée classe d'équivalence.
            Une classe  d'équivalence est évaluée  en un ensemble  de caractères
            voisins (i.e. identiques à un accent ou signe diacritique près).

# Patterns divers (utiles)

Vim peut utiliser 2 moteurs de regex:

   1. un vieux, qui supporte tout (qualifié de backtracking par :h nfa)

   2. un nouveau moteur NFA (Nondeterministic Finite Automatons) qui travaille
      plus vite sur certains patterns, mais ne supporte pas tout

TODO: Does the fact that the old engine is documented as backtracking implies that the new one is not?

It does not seem to be the case.
It seems that the new engine *is* backtracking:

Regex:

    \%#=2\u\{2,},\@!

Text:

    ABC,
    DEF
    GHI,
    JKL

The regex finds `AB`, `DEF`, `GH`, `JKL`.
The fact that it finds `AB` and `GH` seems to suggest that it backtracked.
Unless it uses some optimized algorithm which  can produce the same results as a
backtracking engine, without having to backtrack...

---

Vim sélectionne automatiquement le moteur qu'il juge le plus adapté.
Mais si  on rencontre un pb,  pour tenter de  le déboguer, on peut  préfixer son
pattern avec:

    \%#=1    vieux moteur
    \%#=2    nouveau moteur NFA

Le texte matché  par une regex peut être complètement  différent selon le moteur
qu'on utilise.
Pour une liste de qques pbs qu'on peut rencontrer avec une regex, en fonction du
moteur utilisé, voir `:lh NFA` et plus particulièrement `:h todo /regexp problems`.

Exemple de différences entre les 2:

    (1)    %s/^\(.*\n\)\1\+/\1/        (4)    %s/^\(.*\n\)\1\{1,}/\1/

    (2)    %s/\%#=1^\(.*\n\)\1\+/\1/   (5)    %s/\%#=1^\(.*\n\)\1\{1,}/\1/
    (3)    %s/\%#=2^\(.*\n\)\1\+/\1/   (6)    %s/\%#=2^\(.*\n\)\1\{1,}/\1/


Cette substitution ayant pour but de réduire des séquences de lignes identiques,
ne produit pas le même résultat suivant le multi et le moteur de regex utilisé:

             2,4,5    1,3,6
        foo    foo    foo
        foo    bar    foo
        foo    qux    bar
        foo           bar
        bar           qux
        bar
        bar
        bar
        qux

Les commandes 2, 4 et 5 réussissent tandis que 1, 3 et 6 échouent.

En réalité, la bonne commande pour réduire des séquences de lignes identiques serait:

    %s/^\(.*\)\(\n\1\)\+/\1/

En effet, les  précédentes commandes ne peuvent correctement gérer  le cas d'une
ligne doublon  lorsqu'elle se trouve  tout à la fin  du buffer et  qu'elle n'est
donc pas suivi d'un newline.
Le  1er groupe  capturé ne  doit pas  contenir de  newline pour  pouvoir matcher
n'importe quelle ligne doublon, même en fin de buffer.

Bizarrement, ce coup-ci, peu importe le multi (`+` ou `{1,}`), et peu importe le
moteur, ça marche toujours.
Morale de l'histoire: ne jamais mettre de newline dans une capture à laquelle on
se réfère ensuite?

---

    [\u2000-\u200a]

            All the weird whitespace whose code point is between `U+2000` and `U+200a`.
            Shows that you write an arbitrary range of unicode characters.


    [^\x00-\x7f]

            ensemble des caractères non ascii

            Dans un ensemble de caractères ([...]), \x00 et \x7f correspondent aux
            caractères dont  les points de  code sont 00  et 7f (exprimés  via 2
            chiffres en hexa via l'atome \x).
            Donc:

                    [\x00-\x7f]     rangée de caractères regroupant tous les caractères ascii (0 à 127)
                    [^\x00-\x7f]    ensemble des caractères non ascii

            Question: What's the difference between that and `[[:graph:]]`?
            Only the space character (which is absent from `[[:graph:]]`)?


    [^\x00-\xff]

            ensemble des caractères absents de la table ascii étendue (0 à 255)

            Cette fois, on exclue aussi les caractères accentués.

            Le  précédent  pattern  ([^\x00-\x7f])  et  celui-ci  permettent  de
            trouver  les  caractères spéciaux  /  'exotiques'  présents dans  un
            fichier.
            Pex,  dans  le très  long  fichier  présent, en  excluant  également
            (\u2015 et \u2026), c'est-à-dire en utilisant le pattern suivant:

                    [^\x00-\xff\u2015\u2026]

            ... on ne trouve qu'un nb limité de caractères spéciaux (une centaine atm).


    let pattern_broad  = '...'
    let col            = col('.')
    let pattern_narrow = pattern_broad..'\%(.*\%'..col..'c\)\@!'

            `pattern_narrow` permet  de trouver le  1er match décrit  par `pattern_broad`
            contenant le caractère où se trouve le curseur.

            Décomposition:

                    1. pattern_broad              pattern sans restriction

                    2. '\%(.*\%'..col..'c\)\@!'   restriction:
                                                  le curseur ne doit pas se trouver après le match


            Cette syntaxe permet de facilement exprimer la condition:
            “le curseur doit se trouver qq part au milieu du match“

            Sans elle, il faudrait sans doute passer par une laborieuse suite de
            branches,  chacune  exprimant une  position  possible  au sein  d'un
            sous-pattern de `pattern_broad`.
            La méthode produirait des  patterns de + en + complexes  au fur et à
            mesure que `pattern_broad` serait lui-même complexe.

            S'il peut y avoir plusieurs  matchs différents contenant le curseur,
            et qu'on les veut tous, on  pourrait préfixer le pattern avec une 2e
            restriction comme ceci:

                    '\v%(%'..col..'c.*)@<!'.pattern_broad.'%(.*%'..col..'c)@!'
                     ├───────────────────┘
                     └ le curseur ne doit pas se trouver avant le match.


    \v^%(\s*".*)@!.*\zsfoo

    \v^%(\s*".*)@=.*\zsfoo

            Un `foo` sur une ligne non commentée, dans un fichier Vim.

            Idem mais sur une ligne commentée.

            On pourrait mettre l'ancre `^` à l'intérieur des multi `%()@!` / `%()@=` mais dans ce cas
            la recherche serait bcp plus lente.

            On peut le vérifier en comparant la sortie des 2 commandes qui suivent:

                    :1000Time /\v%(^\s*".*)@=.*\zsfoo    ✘ slow
                    :1000Time /\v^%(\s*".*)@=.*\zsfoo    ✔ fast


    \v(^\s*$|%^)\_s*\zs\S

            matche tous les 1er caractères non whitespace des paragraphes

            Un  début  de  paragraphe  correspond   à  un  non  whitespace  (\S)
            éventuellement précédé sur la même  ligne de whitespace (\_s*), mais
            uniquement si la ligne d'avant (\zs)  est une ligne vide (^\s*$), ou
            si on est au début du buffer (%^).

            On inclut le newline dans \s (\_s)  car il y en a forcément un entre
            la 1e ligne du paragraphe et la ligne vide précédente.
            En effet, l'ancre $ n'en ajoute pas un, elle se contente de dire que
            le caractère suivant en est un.
            Ici, elle dit que le 1er caractère décrit par \_s* est un newline.


    \v.\ze\n\s*$

            matche tous les derniers caractères des paragraphes

            Une fin de paragraphe correspond à  un caractère qcq (.) suivi d'une
            ligne vide,  càd 2  newlines consécutifs éventuellement  séparés par
            des whitespace (\n\s*$).

                                               NOTE:

            Ça ne devrait pas matcher le dernier caractère du dernier paragraphe
            si celui-ci  n'est pas suivi  d'une ligne vide,  car dans ce  cas il
            n'est pas suivi d'un newline.
            On devrait avoir besoin de l'atome %$.
            Pourtant ça marche sans lui.

            On retrouve ce phénomène étrange dans le cas suivant:

                    hello world    : buffer contenant une seule ligne

                    /.\ze\n        : matche le 'd' de 'world'
                    /\n.\zs        : NE matche PAS le 'h' de 'hello'

            Explication possible:    un buffer se termine tjrs par un newline.
            En revanche, il ne commence jamais par un newline

    \v<(\w+)\s+\1>

            matche 2 mots qui se répètent (séparés par des whitespace)
            Illustre qu'on peut utiliser une backref au sein même d'un pattern.

    foo\ze[^(]*)    \vfoo([^(]*\))@=

            matche un foo qui se situe qq part à l'intérieur de parenthèses

            Limite de la regex: en cas  de parenthèses imbriquées, seuls les foo
            à l'intérieur des parenthèses les + profondes sont matchés.

                                               NOTE:

            Il est  difficile de décrire un  pattern qui se situe  à l'intérieur
            d'un niveau intermédiaire d'imbrications de symboles.

            Ex: foo dans    hello ( foo ( world ) )

    \vfoo([^(]*\))@!

            matche un foo qui se situe qq part à l'extérieur de parenthèses

            Peut se lire comme ceci:
            un foo qui ne doit pas  être suivi (@!) d'une parenthèse fermée (\))
            sans aucune parenthèse ouverte avant ([^(]*).

            Limite de la regex: en cas  de parenthèses imbriquées, seuls les foo
            à l'intérieur des parenthèses les + profondes sont exclues.

            Plus généralement, qd  on cherche un pattern qui ne  peut être suivi
            de B qu'à condition que A l'accompagne:

                    \vpattern(ĀB)@!    Je ne veux pas voir B sans A juste avant.
                    \vpattern(Ā*B)@!   Je ne veux pas voir B sans A qq part avant.
                !=  \vpattern(B)@!     Je ne veux pas voir B.

            Ici A = ( et B = )


Étant donné la ligne suivante:    FooBar baz QuxNorf

    \u

            n'importe quelle majuscule

    ^.\{-}\zs\u

            1e maj

    .*\zs\u

            dernière maj

    baz.\{-}\zs\u

            première maj après baz

    .*\zs\u\ze.*baz

            dernière maj avant baz (.{-} à la place du 2e .* marcherait aussi)

    \u\%(.*baz\)\@=
    \u\ze.*baz

            toutes les maj avant baz

            Plusieurs syntaxes sont possibles, car la maj est tjrs matchée en 1ère,
            on décrit la présence de baz qq part après.
            On pourrait remplacer .* par .\{-}, ça marcherait tjrs.

    \%(baz.*\)\@<=\u

            toutes les majuscules après baz

            Dans \%(baz.*\)\@<=\u, .* est dans un lookbehind qui n'est matché qu'après \u.
            Dans baz.*\zs\u, .* est matché avant \u.
            Ceci illustre une différence fondamentale entre \zs et ()@<=.
            Ces atomes ne sont pas matchés au même moment par rapport au reste du pattern.

            Ici, une seule syntaxe est possible, car c'est la seule dans laquelle la maj est matchée en 1e.

            Avec `baz.*\zs\u`, on matcherait seulement la dernière maj après baz.
            Avec `baz.\{-}\zs\u`, on matcherait seulement la 1e maj après baz.
            Ces 2 dernières syntaxes ne marchent pas car une fois qu'un match est trouvé,
            le moteur de regex avance, il ne cherche pas un nouveau match au même endroit.
            S'il y a une autre maj sur la ligne après un autre baz, il la trouvera.
            Mais il ne trouvera pas plusieurs maj entre 2 baz consécutifs.

            See here for another fundamental difference between `\zs` and `\@<=`:

                    https://vi.stackexchange.com/a/16279/17449

            Basically, `\@<=` is a zero-width atom, which means that any text to
            which it applies is considered to have no length.
            This can lead to unexpected results if you apply it to an expression
            using an atom refering to a column position.

            ---

            You can check the difference between `\zs` and `\@<=` with this text:

                foo A B C bar D E F

            If you look for `bar.*\zs\u`, you'll only get `F`.
            If you look for `bar.\{-}\zs\u`, you'll only get `D`.
            If you look for `\%(bar.*\)\@<=\u`, you'll only get `D`, `E`, and `F`.

##
# Reference

[1]: https://regex101.com/
