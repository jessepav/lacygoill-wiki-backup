Purpose:

We have a text containing numbers whose precision can be too big.
We want to limit the precision to 2 or 3 digits after the comma:

    1.23456789
    1.234˜

    1.23000000
    1.23˜

In Vim, we could execute:

    %s/\(\.\d\d[1-9]\?\)\d*/\1/gc

But if the  regex engine finds a  number which has already  the right precision,
like `1.234`, it will still do a - useless - substitution.

To prevent it, we could be tempted to replace the quantifier `*` with `+`:

    %s/\(\.\d\d[1-9]\?\)\d\+/\1/gc

But it would wrongly replace `1.234` with `1.23`.

The issue is not due to `?` being greedy.
Even if it was lazy, the wrong substitution would still be performed:

    %s/\(\.\d\d[1-9]\{-,1}\)\d\+/\1/gc
                    ├────┘
                    └ non-greedy equivalent of `?`

The issue is that an overall match takes precedence over an overall non-match.
IOW,  with lazy/greedy  quantifiers, you  can't  prevent the  regex engine  from
trying every possible path.
Neither greediness nor laziness influence which paths can be checked, but merely
the order in which they are checked.

The solution is to use the possessive quantifier `\@>`:

        %s/\(\.\d\d\%([1-9]\?\)\@>\)\d\+/\1/gc
                               ^-^

When  a possessive  quantifier  is  applied to  an  atomic  grouping (like  here
`\%([1-9]\?\)`), whatever  text was  matched within it  is now  one unchangeable
unit, to be kept or given back only as a whole.

All  saved  states  representing  untried options  within  the  parentheses  are
eliminated, so backtracking can never undo any of the decisions made within.

