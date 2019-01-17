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

##
# Which condition must the character BEFORE an abbreviation satisfy, for the abbreviation to be expanded?

It must be either:

    • a whitespace
    • a beginning of line (yes, it's not a real character then...)
    • outside 'isk' and the abbreviation is full-id
    • in 'isk' and the abbreviation is end-id
    • anything, but the abbreviation is written right after entering insert mode

# Which condition must the character AFTER an abbreviation satisfy, for the abbreviation to be expanded?

It must not be in 'isk', or it must be `C-]`.

#
# How to prevent an abbreviation from being expanded?

Insert the trigger literally:

        C-v SPC

# How to clear all buffer-local abbreviations in command-line mode?

        :cabc[lear] <buffer>

# How to expand an abbreviation without a space being inserted at the end?  (2)

Press `C-]`.

---

Or, in the definition of your abbreviation, consume the space with `getchar()`.

Example:

       fu! s:eat_space() abort
           let c = nr2char(getchar(0))
           return c =~# '\s' ? '' : c
       endfu
       inorea <silent> if  if ()<left><c-r>=<sid>eat_space()<cr>

For more info, see `:helpgrep Eatchar`.

---

What does the `0` argument passed to `getchar()` mean?
It prevents `getchar()` from waiting for a character in the typeahead buffer:

        • if there's one, it consumes it
        • if there's none, it bails out

Is it necessary here?
Probably not.
But it can  be useful when you  use `getchar()` to consume a  character which is
not supposed to  be typed by the  user manually, and for which  there's no sense
waiting.

