# What are the 3 types of abbreviations?

    ┌─────────┬─────────────────────────────────────────┬────────────────┐
    │ type    │ description                             │ examples       │
    ├─────────┼─────────────────────────────────────────┼────────────────┤
    │ full-id │ all the characters must be in 'isk'     │ foo   g3   -1  │
    ├─────────┼─────────────────────────────────────────┼────────────────┤
    │ end-id  │ the last character must be in 'isk',    │ #i   ..f   $/7 │
    │         │ the other ones must NOT                 │                │
    ├─────────┼─────────────────────────────────────────┼────────────────┤
    │ non-id  │ the last character must NOT be in 'isk' │ def#   4/7$    │
    │         │ the others can be in 'isk' or not       │                │
    └─────────┴─────────────────────────────────────────┴────────────────┘

#
# Which condition must the character BEFORE an abbreviation satisfy, for the abbreviation to be expanded?

It must be either:

   - a whitespace
   - a beginning of line (yes, it's not a real character then...)
   - outside 'isk' and the abbreviation is full-id
   - in 'isk' and the abbreviation is end-id
   - anything, but the abbreviation is written right after entering insert mode

# Which condition must the character AFTER an abbreviation satisfy, for the abbreviation to be expanded?

It must not be in `'isk'`, or it must be `C-]`.

#
# How to prevent an abbreviation from being expanded?

Insert the trigger literally:

    C-v SPC

# How to clear all buffer-local abbreviations in command-line mode?

    :cabc[lear] <buffer>

##
# How to manually expand an existing abbreviation without a space being inserted at the end?

Press `C-]`.

## How to redefine my abbreviation so that it's done automatically?

In the rhs of the abbreviation, consume the space with `getchar()`.

Example:

    fu s:eat_space() abort
       let c = nr2char(getchar(0))
       return c =~# '\s' ? '' : c
    endfu
    inorea <silent> if if ()<left><c-r>=<sid>eat_space()<cr>

Here's what happens:

   - you type `i`; it's written in the typeahead buffer, then executed (i.e. inserted in the user buffer)
   - you type `f`; same thing

   - you type space:

       * it's written in the typeahead buffer
       * Vim checks whether the text before the cursor matches an abbreviation
       * it finds one, and removes `if` in the typeahead buffer
       * `if ()<left><c-r>=<sid>eat_space()<cr>` is written in the typeahead buffer
       * the typeahead buffer is executed
       * when `<sid>eat_space()` is processed, the space is still in the typeahead buffer (right after),
         and `getchar()` consumes it
       * the typeahead buffer is now empty, and the space is not executed (i.e. inserted in the user buffer)

You may wonder why `if ()...` is written in the typeahead buffer.
I think  it has  to, because if  you define a  recursive abbreviation  (`iab` vs
`inorea`), mappings are applied; that can only happen in the typeahead buffer.

For more info, see `:helpgrep Eatchar`.

---

You could probably replace this line:

    return c =~# '\s' ? '' : c

With:

    return c

However, if  you were to  use `s:eat_space()`  in another abbreviation,  and for
some  reason you  wanted to  use it  in  a different  position in  the rhs,  the
function  could wrongly  consume some  non-whitespace character  which would  be
unexpected.   So the  current statement,  while not  necessary here,  is a  good
practice.

---

The  fact  that  `getchar()`  consumes   the  typeahead  buffer  is  not  really
documented, but it's briefly mentioned at `:h :map-<expr> /typeahead`:

>     You can use getchar(), it consumes typeahead if there is any.

Besides, from where else would `getchar()` consume a key?

### Why the `0` argument?

                            v
    let c = nr2char(getchar(0))

It  prevents the  latter from  waiting  for a  character  to be  written in  the
typeahead buffer when the latter is empty:

   - if there's one, it consumes it
   - if there's none, it bails out

It's necessary when you expand an abbreviation via `C-]`.
This suggests that `C-]`  is not written in the typeahead  buffer (but the space
is, which is expected).

