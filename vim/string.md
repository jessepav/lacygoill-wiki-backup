# What's a newline?

Any character or set of characters used to represent a new line:

    ┌───────┬─────────┐
    │ CR LF │ Windows │
    ├───────┼─────────┤
    │ LF    │ Unix    │
    └───────┴─────────┘

# What's the only option which alters the behavior of `match()` and `matchstr()`?

`'ignorecase'`

Which is why  you should always use `\c`  or `\C` in your pattern,  to avoid any
influence from the current environment.

##
# Coercion
## I have an expression containing a math operator (`+`, `<`, ...) and a string.

    'hello' + 123
    'hello' < 123
    ...

### How is the string evaluated when it begins with
#### a letter?

    0

---

    echo 'hello' + 123
    123~

#### an integer?

This integer.

---

    echo '12hello' + 3
    15~

#### a float?

Its integer part.

---

    echo '12.34hello' + 5
    17~

###
## How to convert a string into a float?

Use `str2float()`:

    echo str2float(str)

---

    echo str2float('1.2') + 3
    4.2~

    echo str2float('1.2foo') + 3
    4.2~

## Can I use a number as a key in a dictionary?

Yes.

          v
    echo {1: 'one'}
    {'1': 'one'}~

                      v
    echo {'1': 'one'}[1]
    one~

Whether you use  the number when you  define the dictionary, or when  you try to
access some of its value, Vim will coerce it into a string.

##
## Which pitfall should I avoid when relying on Vim's builtin coercion of strings into numbers?

If the  number inside the  string begins  with `0`, and  if its digits  don't go
beyond `7`, it will be interpreted as octal.

    echo '017' + 1
    16~

To fix this, use `str2nr()`:

    echo str2nr('017') + 1
    18~

---

`str2nr()` takes  a string containing  a number as  input, and converts  it into
decimal.

It accepts a second optional argument which stands for the input base.
Without it, `str2nr()` assumes that your input number is decimal; which explains
the output of:

    echo str2nr('017')
    17~

### When should I be conscious of it?

Whenever you perform a substitution, and you use `submatch()` in the replacement
part to refer to a capturing group matching a number.

User data is unpredictable; you have to assume a decimal number may begin with `0`.

####
# Special notations
## Why is the caret notation of
### a null `^@`?

It has  been decided to  represent the  first control character  (codepoint `1`)
with the first letter of the alphabet; so, the caret notation of `SOH` (Start Of
Heading) is `^A`.

The null is a special control character whose codepoint is `0`.
To go  on using the same  scheme, it has been  decided to represent it  with the
letter which comes before `A` in the ascii table, which is `@`.

### escape `^[`?

The codepoint of escape is `27`.
The previous codepoints are represented with `A-Z`.
To go on using  the same scheme, it has been decided  to represent `Escape` with
the first character after `Z` in the ascii table, which is `[`.

###
## What's the caret notation of the delete character?

    ^?

#### Which key emits it?

The backspace key.

Don't confuse the delete character with the delete key.
<https://en.wikipedia.org/wiki/Delete_character>

##
## Which escape sequences can I use to encode an arbitrary character?  (3)

    \x..
    \u....
    \U........

The dots stand for hexadecimal digits,  and must match the hex/unicode codepoint
of the character.

---

    echo "a \x26 b"
    echo "a \u26 b"
    echo "a \U26 b"
    a & b~

In this string, you can use 2 digits only, even with `\u` and `\U`.
But that's only because the next character is a space, which is not a hex digit.
If the next character *was* a hex digit, you would have to add a padding of `0`'s:

    echo "a \u00261b"
    echo "a \U000000261b"
    a &1b~

##
# echo
## What's the output of
### `:echo "ab\rc"`?

    cb~

`:echo`  has printed  `ab`,  then `\r`  made  it  move the  cursor  back to  the
beginning of the line, then it has printed `c`.

### `:echom "ab\rc"`?

    ab^Mc~

`:echom` never interprets anything, so `\r` doesn't make it move the cursor.

##
## How to print two messages without adding any character between them?

Use `:echon`:

    echon 'foo' 'bar'
    foobar~

    echon 'foo' | echon 'bar'
    foobar~

    :echo 'foo' 'bar'
    foo bar~

    :echo 'foo' | echo 'bar'
    foo~
    bar~

##
# Extract characters
## How to get the `n`-th
### byte of a string?  (2)

Use `strpart()`:

    echo strpart(str, n-1, 1)
                      ├─┘  │
                      │    └ {len}
                      └ {start}

Or index the string directly:

    echo str[n-1]

---

    echo strpart('résumé', 2, 1)
    <a9>~

    echo 'aéb'[1]
    <c3>~

---

`str[n-1]` is not evaluated into the character of index `n-1`, but the *byte* of
index `n-1`.

Here, the  byte of index `1`  is not a  complete character, because `é`  takes 2
bytes instead of 1.
So,  Vim   prints  the  special   sequence  `<c3>`  which  is   the  hexadecimal
representation of the first byte of `é`:

    $ xxd -p -l2 <<<'é'
    c3a9~

### character of a string?  (2)

Use `strcharpart()`:

    echo strcharpart(str, n-1, 1)
                          ├─┘  │
                          │    └ {len}
                          └ {start}

Or `strgetchar()` + `nr2char()`:

    echo nr2char(strgetchar(str, n-1))
                                 ├─┘
                                 └ {index}

---

    echo strcharpart('résumé', 2, 1)
    s~

    echo nr2char(strgetchar('résumé', 2))
    s~

##
## How to get the last characters of a string, from the `n`-th one?

Use `strcharpart()`, but don't provide the last optional argument `{len}`:

    echo strcharpart(str, n-1)

Without `{len}`, `strcharpart()` goes until the end.

---

    echo strcharpart('abcde', 1)
    bcde~

###
## What's the evaluation of `getline('.')[col('.')]`?

The character right *after* the cursor.
If the  latter is multibyte,  then, the expression  evaluates to its  first byte
instead.

### Why is it not the character under the cursor?

`col('.')` adds `1` to the byte index of the character under the cursor;
probably because `0` is already used for an error:

> The first column is 1.  0 is returned for an error.

---

The same is true for `\%123c`.
To match the first character on a line, you must use `\%1c.` and not `\%0c.`.

#### Why can't the expression be tweaked to get it?

Because it could be a multibyte character.

So you can't know how much you must remove from `col('.')`.

As an example, position your cursor on the first `é` in this text:

    résumé
     ^

And execute:

                              vv
    echo getline('.')[col('.')-1]
    <c3>~

#### How to get it then?

Use `matchstr()`, `col('.')` and `\%123c`:

    echo matchstr(getline('.'), '\%'.col('.').'c.')

`\%123c` means that the byte index of the next character is `123`.
`col('.')` returns the byte index of the character under the cursor.

#
## Negative index
### How is a negative index argument interpreted by
#### most functions handling a string?

`0`

#### `strcharpart()`?

A  negative index  is  *not* replaced  by  `0`,  but since  there  can't be  any
character with a negative index in a string, it produces empty strings.

    echo strcharpart(str, -i, j)
    ⇔
    echo strcharpart(str, 0, j-i)

---

    echo strcharpart('abcd', 0, 2)
    ab~

    echo strcharpart('abcd', -2, 4)
    ab~

   • character of index -2 = ''
   • character of index -1 = ''
   • character of index 0  = 'a'
   • character of index 1  = 'b'

###
### What's the evaluation of
#### `str[-i]`?

An empty string.

#### `str[-i:-j]` with `0 < i < j`?

An empty string.

#### `str[-i:-j]` with `0 < j < i`?

The last bytes of the string.

    echo 'abc'[-2:-1]
    'bc'~

##
# Getting info
## How to get a substring matching a pattern
### starting `{start}` bytes after the beginning of the original string?

Use the third optional argument of `matchstr()`:

    echo matchstr(str, pat, start)

---

    echo matchstr('-a -b -c', '-.', 3)
    -b~

Here, we start the search 3 bytes after the beginning of the string:

    -a -b -c
       ^
       the search start here

#### and only the `{count}`-th occurrence of a match?

Use the fourth optional argument: `{count}`:

    echo matchstr(str, pat, start, count)

---

    echo matchstr('-a -b -c -d', '-.', 3, 2)
    -c~

Here, the  first match  is `-b`, but  we ask  for the second  match, so  `-c` is
returned.

##
## Which other functions accept the optional arguments `{start}` and `{count}`?  (4)

   - `match()`
   - `matchend()`
   - `matchlist()`
   - `matchstrpos()`

---

    echo match('-a -b -c', '-.', 2, 2)
    6~

Here, we ignore the first 3 bytes (index 0, 1 and 2), and the first match (`-b`).

###
## How to get the byte index position of
### the start of a text described by a regex inside a string?

Use `match()`:

    echo match(str, pat)

---

    echo match('Starting point', '\cstart')
    0~

`start` was found at the very beginning.

#### its end?

Use `matchend()`:

    echo matchend(str, pat)

---

    echo matchend('Starting point', '\cstart')
    5~

####
### the first occurrence of a literal text inside a string?

Use `stridx()`:

    echo stridx(str, substr)

---

    echo stridx('Starting point', 'start')
    -1~

`start` was not found.

#### and ignore the first `n` bytes?

Use the optional third argument, `{start}`:

    echo stridx(substr, str, start)

---

    echo stridx('abc abc', 'b')
    1~

    echo stridx('abc abc', 'b', 2)
    5~

###
### the last occurrence of a literal text inside a string?

Use `strridx()`:

    echo strridx(str, substr)

---

    echo strridx('a:b:c', ':')
    3~

#### and ignore the bytes after the `n`-th one?

Use the optional third argument, `{start}`:

    echo strridx(substr, str, start)

---

    let str = 'a:b:c:d'
    let colon_last = strridx(str, ':')
    let colon_before_last = strridx(str, ':', colon_last - 1)
    echo colon_before_last
    3~

###
## How to get the byte index of the start and end of a match inside a string?

Use `matchstrpos()`:

    echo matchstrpos(str, pat)

---

    echo matchstrpos('-a -b -c', '-.')
    ['-a', 0, 2]~

    echo matchstrpos('-a -b -c', '-.', 3)
    ['-b', 3, 5]~

    echo matchstrpos('-a -b -c', '-.', 3, 2)
    ['-c', 6, 8]~

---

The last number in the output is the byte index of the end of the match **plus** `1`.

###
## How to get the number of times a substring appears in a string?

    echo count(str, substr)

---

    echo count('-a -b -c', '-')
    3~

### Can it work with a regex?

No.

    echo count('-a -b -c', '-.')
    0~

### How to ignore the case?

Pass a non-zero value as a third optional argument:

    echo count(str, val, 1)
                         ^

---

    echo count('abA', 'a')
    1~

    echo count('abA', 'a', 1)
    2~

### What happens if the string contains overlapping occurrences of the substring?

`count()` only considers *non* overlapping occurrences.

    echo count('aaa', 'aa')
    1~

    echo count('aaaa', 'aa')
    2~

###
## How to get the number of characters stored in a string?

    echo strchars(str, 1)

---

The second  argument is optional,  but it's necessary  if the string  contains a
composing character:

    echo strchars('Ë͙͙̬̹͈͔̜́̽D̦̩̱͕͗̃͒̅̐I̞̟̣̫ͯ̀ͫ͑ͧT̞Ŏ͍̭̭̞͙̆̎̍R̺̟̼͈̟̓͆')
    51~

    echo strchars('Ë͙͙̬̹͈͔̜́̽D̦̩̱͕͗̃͒̅̐I̞̟̣̫ͯ̀ͫ͑ͧT̞Ŏ͍̭̭̞͙̆̎̍R̺̟̼͈̟̓͆', 1)
    6~

##
## How to get the number of cells a character occupy?

    echo strwidth(char)

### What if this number changes depending on where the character is put on the current line?

    echo strdisplaywidth(char, col)

---

This is useful for a tab:

    echo strdisplaywidth("\t", col('.')-1)
                                       ├┘
                                       └ Probably for the same reason we need to remove 1 in:

                                             getline('.')[col('.')-1]

##
## I have a string and a pattern.  How to get the list of substrings matching the capturing groups?

Use `matchlist()`:

    echo matchlist(str, pat)

---

    echo matchlist('abcd', '\v(.(.))(.)')
    ['abc', 'ab', 'b', 'c', '', '', '', '', '', '']~
      │      │     │    │
      │      │     │    └ \3
      │      │     └ \2
      │      └ \1
      └ \0

##
# Time
## How to get the local time in seconds since the epoch?

    echo localtime()
    1548170168~

### How to make it human-readable?

    echo strftime('%c', localtime())

Here,  you  don't  need  `localtime()`,   because  without  a  second  argument,
`strftime()` assumes the current time:

    echo strftime('%c')

#### with the format `year-month-day`?  (2)

    echo strftime('%F')
    echo strftime('%Y-%m-%d')
    2019-01-22~

#### with the format `hour:min:sec`?  (2)

    echo strftime('%T')
    echo strftime('%H:%M:%S')
    16:16:28~

#### Where can I find all the possible formats?

    $ man strftime

#
## How to get a human-readable date of the epoch?

    echo strftime('%c', 0)
    Thu 01 Jan 1970 01:00:00 AM CET~

---

The hour is not `00:00:00` because of our timezone; where we live, we must add 1 hour:

                   ┌ The +hhmm or -hhmm numeric timezone (that is, the hour and minute offset from UTC
                   ├┐
    echo strftime('%z')
    +0100~

##
## How to get more precision (up to a millionth of a second)?

    echo reltime()
    [1548170958, 895512]~
     ├────────┘  ├────┘
     │           └ millionths of a second
     └ seconds since epoch

### The output is a list.  How to get a string instead?

Use `reltimestr()`:

    echo reltimestr(reltime())

##
## How to get the time passed between
### now and a previous date?

`reltime()`  accepts an  optional  argument,  `{start}`, which  must  be a  list
representing a date.

When provided, `reltime()` computes the time passed between this date and now.

    echo reltime(date)

---

    let date = reltime()
    let duration = reltime(date)
    echo reltimestr(duration)
    0.000009~

### two dates?

`reltime()` accepts  a second optional argument,  `{end}`, which must be  a list
representing a date.

When provided, `reltime()` computes the time passed between `{start}` and `{end}`.

    echo reltime(date1, date2)

---

    let date1 = reltime()
    let date2 = reltime()
    let duration = reltime(date1, date2)
    echo reltimestr(duration)
    0.000007~

##
## How to get the date of the last modification of `file`?

    echo getftime('file')
    1548170113~

    echo strftime('%c', getftime('file'))
    Tue 22 Jan 2019 04:18:26 PM CET~

##
# execute()
## Does the second argument of `execute()` has an influence on
### the evaluation of the first argument?

Yes.
It can be used to prevent Vim from printing any message:

    :call execute('echom "hello"')
    ∅~
    :call execute('echom "hello"', 'silent')
    ∅~
    :call execute('echom "hello"', 'silent!')
    ∅~

    :echo execute('echo "hello"')
    :echo execute('echo "hello"', 'silent')
    :echo execute('echo "hello"', 'silent!')
    hello~

### the output of `execute()`?

Most of the time, no.

However, there's one exception.
If you use `silent!`, the error messages won't be included in the output.

    echo execute('abcd', 'silent!') is# ''
    1~

###
## How to eliminate the newline at the beginning of `execute('ls')`?

    echo execute('ls')[1:]

##
# Transforming
## Splitting
### How to get the list of words on the line?

    echo split(getline('.'), '\%(\k\@!.\)\+')

### Is the output of `split()` different if the pattern matches at the very beginning/end of the string?

By default, no.

But it can be if you add the optional argument `{keepempty}`:

                            v
    echo split(':a:b', ':', 1)
    ['', 'a', 'b']~

    echo split('a:b:', ':', 1)
    ['a', 'b', '']~

    echo split(':a:b:', ':', 1)
    ['', 'a', 'b', '']~

### Why do `join()` and `split()` process `\n` differently, when passed as a second argument?

    echo split("a\nb", '\n')
    ['a', 'b']~

    echo join(['a', 'b'], '\n')
    a\nb~

Theory:

`split()` expects a regex, so `'\n'` is fine.
`join()` expects a literal string, so `'\n'` doesn't work.

##
## Translating
### How to replace a set of characters with another set in a given string?

Use `tr()`:

    echo tr()

---

    echo tr('big bad wolf', 'bw', 'BW')
    Big Bad Wolf~

    echo tr('<blob>', '<>', '{}')
    {blob}~

### How to make Vim translate special sequences such as `\<tab>` or `\x26` in a literal string?

Concatenate double quotes at the beginning and end of the string.
Then use `eval()`.

    let string = 'foo \x26 bar'
    echo eval('"'.string.'"')
    foo & bar~

    let string = 'foo\<tab>bar'
    echo eval('"'.string.'"')
    foo    bar~

---

`eval()` expects a string as argument.
`"string"` is *still* a string, so our concatenations didn't cause an issue.

`eval()` looks at what is inside its string argument, and evaluates it.
For example, if it was `&ft`, it would return `markdown`.

Here, it  finds `"string"`, whose  evaluation is the  same string, but  with the
surrounding quotes removed and the special characters translated.

### How to translate all unprintable characters in a string?

    echo strtrans(str)

---

    echo strtrans("a\nb")
    a^@b~

##
# Issues
## `:echo 'hello' " some comment` raises `E114`!

    echo 'hello' " some comment
    E114: Missing quote: " some comment~

`:echo[m]` sees a double quote as part of its argument.
Therefore, you can't append a comment like you could with other commands:

    :y_ " some comment

You need a bar to explicitly tell  `:echo[m]` that what follows is *not* part of
its argument; see `:h :comment`.

    echo 'hello' | " some comment
    hello~

##
##
##
# ?

When  you  try   to  extract  some  text  around  the   cursor  position,  avoid
`virtcol('.')`; it's not reliable.

To illustrate, write this sentence in `/tmp/file`:

    they would be useful if they were here

Then, start Vim like this:

    $ vim -Nu NONE +'norm! 13l' +'lefta 20vs | setl wrap lbr' /tmp/file
    :echo strcharpart(getline('.'), virtcol('.') - 1, 3)
    l SPC i~

You probably expected `SPC u s`.
The reason for this difference is explained in `./vimL.md`.

Basically, if  there is a  column where no real  character resides in  the file,
between 2  other columns where  there *are* real  characters, the column  in the
middle is *not* ignored.

Although, I guess it's ok to use `virtcol()` when you're sure your lines are *not*
wrapped.

# printf()

`printf()` est une fonction utile pour  manipuler une chaîne au sein de laquelle
on veut:

   • tronquer une sous-chaîne ou un flottant
   • ajouter un padding d'espaces ou de zéros
   • convertir un nb décimal en hexa ou en base 8
   • convertir un code ascii décimal en le caractère lui correspondant

---

    printf({fmt}, {expr1} ...)

`{fmt}` est une chaîne pouvant contenir des items `%`.
Pour chaque item utilisé (sauf `%%`), il faut fournir à `printf()` une
expression correspondante.

`printf()`  retourne la  chaîne  `{fmt}` où  les items  sont  remplacés par  les
expressions.
Les items servent à formater les expressions: on parle d'interpolation.
On ne peut pas utiliser plus de 18 expressions.

Le  formatage  est décrit  par  une  spécification  de  conversion qui  suit  le
caractère `%`.
Il  attend 1  argument obligatoire  (spécificateur  de conversion  aka type)  et
accepte  jusqu'à 3  arguments  optionnels (flags,  field-width, precision)  dans
l'ordre suivant:

    %  [flags]  [field-width]  [.precision]  type

---

    type

Il s'agit d'un caractère spécifiant le type de conversion à appliquer.

    ┌───┬───────────────────────────────────────────────────────────────────────────────────────────────┐
    │ s │ chaîne alignée à droite                                                                       │
    │   │ `field-width` et `.precision` sont interprétés comme des nb d'octets                          │
    │   │                                                                                               │
    │   │ La chaîne n'a besoin d'être alignée que si `field-width` est supérieur                        │
    │   │ au nb d'octets qu'elle pèse.                                                                  │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ S │ idem mais `field-width` et `precision` sont interprétés comme des nb de cellules              │
    │   │                                                                                               │
    │   │ La chaîne n'a besoin d'être alignée que si `field-width` est supérieur                        │
    │   │ au nb de cellules qu'elle occupe.                                                             │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ c │ caractère à partir de son code ascii                                                          │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ d │ nb entier décimal/en base 10                                                                  │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ x │ nb hexa                  caractères minuscules                                                │
    │ X │ nb hexa                  caractères maj                                                       │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ o │ nb octal                                                                                      │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ f │ nb flottant                                                                                   │
    │ e │ nb flottant; notation scientifique:      1.234560e+02                                         │
    │ E │ idem, mais en remplaçant l'exposant 'e' par 'E'                                               │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ g │ nb flottant;                                                                                  │
    │   │ équivalent à f si le nb est compris entre 10^-3 (inclus) et 10^7 (exclus), e autrement        │
    │   │                                                                                               │
    │   │ En l'absence de précision, les zéros superflus (ex: 123.456000) sont supprimés                │
    │   │ (contrairement à f).                                                                          │
    │   │ Un zéro juste après la virgule (123.0) n'est pas superflu, car il caractérise                 │
    │   │ le flottant, et le différencie d'un nb entier.                                                │
    │   │                                                                                               │
    │ G │ idem, mais équivaut à E qd le nb est compris entre 10^-3 et 10^7                              │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ % │ '%%' est converti en '%' (aucun argument à fournir)                                           │
    └───┴───────────────────────────────────────────────────────────────────────────────────────────────┘

---

    flags

Une suite d'un ou plusieurs caractères.

    #

N'a d'effet qu'avec les types `o`, `x` et `X`.

A pour effet d'ajouter en préfixe `0`, `0x` ou `0X`:

    echo printf('%#o', 123)
    0173~
    echo printf('%#x', 123)
    0x7b~
    echo printf('%#X', 123)
    0X7B~

Permet d'exprimer explicitement la base dans laquelle est écrite le nb.

    0

Padding de zéros au lieu d'espaces.
Ne fonctionne que lorsque le padding est à gauche.
Un padding à droite ne peut être constitué que d'espaces.

    -

Alignement à gauche et non à droite.

    +

Préfixe un `+` devant un nb positif:

    echo printf('%+d', 123)
    +123~
    echo printf('%+.2f', 12.34)
    +12.34~

    ' '

Préfixe un espace devant un nb positif:

    echo printf('% d', 123)
    ' 123'~
    echo printf('%+ .2f', 12.34)
    '+12.34'~

`+` a la priorité sur espace.

---

    field-width

`field-width` est un  entier positif spécifiant le poids en  octets de la valeur
convertie.
Sauf pour l'item `%S` où il correspond à une largeur en nb de cellules.

Si `field-width` > poids  en octets de la valeur convertie  (ou nb de cellules),
un padding d'espaces est ajouté à gauche.
Si `field-width` < ..., la valeur n'est *pas* tronquée pour autant.

À la place d'un nb, on peut donner à `field-width` une valeur spéciale `*`.
Dans ce cas, il faudra passer à `printf()` 2 arguments au lieu d'un.
Le 1er correspondant au poids/largeur du champ, le 2e à l'expression à formater.
Ex:

    echo printf('%d: %*s', nr, width, line)

On a bien 2 items (`%d` et `%s`), mais 3 arguments en plus de la chaîne:

   • `nr`     est l'expression formatée selon %d
   • `width`  est le poids du champ dans lequel doit s'afficher `line`
   • `line`   est l'expression formatée selon %*s

`*` est utile lorsqu'on  a besoin d'une largeur de champ  dynamique, et est plus
lisible qu'une concaténation de chaînes:

    let prec = 9

    ✔
    echo printf('%'.prec.'f', 1/3.0)
    ✔✔
    echo printf('%*f', prec, 1/3.0)

---

    .precision

`precision`  est un  nb  interprété  de façon  différente  selon  le type  qu'il
affecte:

   • d, o, x et X     minimum de chiffres à afficher      avec padding (0/espace) si besoin
   • s                maximum d'octets à afficher         troncation si besoin
   • S                maximum de caractères à afficher    "
   • f, e, E, g, G    nb de chiffres après la virgule     "

Les différences d'interprétation sont logiques:  on souhaite souvent tronquer un
flottant, mais pas un entier.

Ceci  étant, pour  obtenir un  padding de  `0` avec  un entier,  il paraît  plus
logique d'utiliser un `field-width` et le flag `0`:

    echo printf('%06d', 123)

plutôt que

    echo printf('%.6d', 123)

Ainsi, on  peut considérer  que field-width  et .precision  ont des  usages bien
distincts:

    field-width = padding
    .precision  = troncation

Si on utilise le  flag `.precision` mais sans lui donner  de valeur (ex: `%.s`),
il est considéré comme valant `0` (=troncation max).

Si on n'utilise pas du tout le  flag `.precision` (ex: `%f`), il est malgré tout
considéré comme valant `6` pour un flottant  de type `f` ou `e`/`E`, et `1` pour
un flottant de type `g`/`G`.

Tout comme  pour `field-width`, on  peut donner à  `precision` la valeur  `*` au
lieu d'un nb.
Et à nouveau, dans ce cas, il faudra fournir 2 arguments au lieu d'un.
Un pour la précision de l'item, et un pour son contenu.

---

                                 ┌─ fonctionne car ...
                                 │
    ┌──────────────────────────┬────────────────────────────────────────────────────────────┐
    │ echo printf('%s',  123)  │ le nb 123 a été initialement converti en la chaîne '123'   │
    │     → '123'              │                                                            │
    ├──────────────────────────┼────────────────────────────────────────────────────────────┤
    │ echo printf('%d', '123') │ la chaîne 123 a été initialement convertie en le nb 123    │
    │     → '123'              │                                                            │
    ├──────────────────────────┼────────────────────────────────────────────────────────────┤
    │ echo printf('%f',  123)  │ le nb 123 a été initialement converti en le flottant 123.0 │
    │     → '123.000000'       │                                                            │
    └──────────────────────────┴────────────────────────────────────────────────────────────┘

`printf()` peut, lorsque c'est nécessaire, convertir un argument d'un type donné
en un autre.
Les seules types de conversions automatiques possibles sont:

   • nb    ↔    chaîne
   • nb    →    flottant

---

    echo printf('this char is %c', 97)
    this char is a~

`%c` permet  d'insérer au sein  d'une chaîne un caractère  à partir de  son code
ascii.


    echo printf('%f', 123.456)
    123.456000~

En l'absence de  précision explicite, printf() considère qu'elle  vaut `6`, d'où
les 6 chiffres après la virgule ici.

---

    echo printf('%.f', 123.456)
    123~

Qd la précision vaut 0 (`.` = `.0`), la partie décimale d'un flottant est omise:

    %.f    ⇔    %.0f

---

    echo printf('%6d', 123)
       123~
    echo printf('%06d', 123)
    000123~

    echo printf('%.s', 'foobar')
    ''~

En l'absence de précision, elle est considérée comme nulle, et précision nulle =
troncation max:

    %.s    ⇔    %.0s

