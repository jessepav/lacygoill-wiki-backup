# What's the meaning of the acronym IEEE?

Institute for Electrical and Electronics Enginners.

## How is it pronounced?

“I triple E.”

##
# What does it mean for a set to be “countable”?

Intuitively:

You can count/enumerate its  elements from one of them to any  other in a finite
amount of time.

The set of real numbers, for example, is UNcountable because you can't enumerate
all the numbers from 0 to 1 in a finite amount of time.
There are more  real numbers between 0 and  1, than in the whole  set of natural
numbers.

---

More formally:

There exists a one-to-one correspondence between this set and the set of natural
numbers; IOW, all of its elements can be written in an enumeration:

    s₁, s₂, s₃, ...

With no infinity in the middle.

So, this is an enumeration of the natural numbers:

    1 3 2 5 4 7 6 ...
                  ^^^
                  allowed

But not this:

    2 4 6 8 ... 1 3 5 7 ...
            ^^^
            forbidden

---

Even more formally:

> A set  S is countable if  there exists an injective  function f from S  to the
> natural numbers N = {0, 1, 2, 3, ...}.

<https://en.wikipedia.org/wiki/Countable_set#Definition>
<https://en.wikipedia.org/wiki/Injective_function>

# How to prove that
## the set of rational numbers is countable?

Imagine them listed in this infinite two-dimensional array:

    ┌─────┬──────┬───────┬───────┬───────┬─────┐
    │     │ 1    │ 2     │ 3     │ 4     │ ... │
    ├─────┼──────┼───────┼───────┼───────┼─────┤
    │ 1   │ ±1/1 │ ± 1/2 │ ± 1/3 │ ± 1/4 │ ... │
    ├─────┼──────┼───────┼───────┼───────┼─────┤
    │ 2   │ ±2/1 │ ± 2/2 │ ± 2/3 │ ± 2/4 │ ... │
    ├─────┼──────┼───────┼───────┼───────┼─────┤
    │ 3   │ ±3/1 │ ± 3/2 │ ± 3/3 │ ± 3/4 │ ... │
    ├─────┼──────┼───────┼───────┼───────┼─────┤
    │ 4   │ ±4/1 │ ± 4/2 │ ± 4/3 │ ± 4/4 │ ... │
    ├─────┼──────┼───────┼───────┼───────┼─────┤
    │ ... │ ...  │ ...   │ ...   │ ...   │ ... │
    └─────┴──────┴───────┴───────┴───────┴─────┘

We need to find an enumeration of all these numbers.

Listing the first line and then the second,  and so on, does not work, since the
first line  never terminates; you can't  enumerate the numbers between  ±1/1 and
±2/1 in a finite amount of time.

But if we list them by diagonal:

    ±1/1
    ±2/1, ±1/2
    ±3/1, ±2/2, ±1/3
    ±4/1, ±3/2, ±2/3, ±1/4
    ...

We get an enumeration.

Indeed, the  table contains all rationals;  so no matter the  rational you think
of, it must be somewhere in the table.

Besides, in this listing, you can reach  any rational number – including the one
you think of – in a finite amount  of time, because the diagonals are all finite
(contrary to the lines and columns).

---

To be able to enumerate this list  without looking at the table, notice that the
sum of the numerator and the denominator  of all rationals in any given diagonal
is constant; and it's increasing by 1  from one diagonal to the next: 2, then 3,
then 4, then 5, etc.

## the set of real numbers is UNcountable?

Use the Cantor's diagonal argument:
<https://en.wikipedia.org/wiki/Cantor%27s_diagonal_argument>

Let's assume that the set of real numbers is countable.
It follows that all of its elements can be written as an enumeration:

    s₁, s₂, s₃, ...

For example, the start of the enumeration could look like this:

    ┌─────┬───────────────────┐
    │ s1  │ .5032164223981... │
    ├─────┼───────────────────┤
    │ s2  │ .0782913601120... │
    ├─────┼───────────────────┤
    │ s3  │ .3111370055629... │
    ├─────┼───────────────────┤
    │ s4  │ .9999261457682... │
    ├─────┼───────────────────┤
    │ s5  │ .0001042507334... │
    ├─────┼───────────────────┤
    │ ... │ ...               │
    └─────┴───────────────────┘

Now, let's build an element `s` by selecting the first decimal in `s₁` plus 1:

    5+1 = 6
    s = .6

then the second decimal of `s₂` plus 1:

    7+1 = 8
    s = .68

then the third decimal of `s₃` plus 1:

    1 + 1 = 2
    s = .682

then the fourth decimal of `s₄` minus 1:

    9 - 1 = 8
    s = .6828

then the fifth decimal of `s₅` plus 1:

    0 + 1 = 1
    s = .68281

Repeat the process  indefinitely, by extracting the `ᵢ`th decimal  of `sᵢ`, `+1`
if it's lower than 8, and `-1` if the decimal is 9.

You get  a real  number `s`,  which is different  than all  the numbers  in your
enumeration.
But since `s` is a real number, it should be somewhere in the enumeration.
This contradiction  implies that the  original assumption  is false: the  set of
real numbers is *not* countable.

##
# Express euler's number as the sum of an infinite series.  (2)

    e = Σ(1/n!), n ≥ 0

    e = Σ(1 + 1/n)^n, n ≥ 1

Note that any irrational number can be expressed as the sum of an infinitie series.

##
# What does the Roman numeric system require?  (3)

A different symbol for each power of 10:

   - X for 10
   - C for 100
   - M for 1000
   - ...

It also requires repetition to indicate how many of each power of 10 is present.

Finally, it requires  additional symbols to abbreviate a group  of 5 consecutive
and identical symbols:

   - V = IIIII
   - L = XXXXX
   - D = CCCCC
   - ...

For example, MDCCCCLXXXV means 1000 + 500 + 400 + 50 + 30 + 5 = 1985.

## What was such a system good for?

Easy transcription of numbers to an abacus for calculation.

## What was such a system *not* good for?  (2)

Calculation with pencil and paper.
Representation of large numbers.

##
# Why is our current numeric system called positional?

Because the meaning of a number is understood from the position of its symbols.

# What does a positional notation require?

The representation of zero by a symbol.
Zero is needed, for example, to distinguish 1 from 10.

# What other positional system do you know and use on a daily basis?

The base 60 system used by the Babylonians.

We use it today in our division of  the hour into 60 minutes and the minute into
60 seconds.

##
# Where does the word “bit” come from?

It's an abbreviation for binary digit.

## How can I view it physically?

As a single physical entity which is either on or off.

# How do you call a string of bits?

A bitstring.

# What can a byte represent?

Up to 256 bitstrings, which may be viewed as representing the integers from 0 to
255, or some characters.

The ASCII  encoding scheme  defines standard  character interpretations  for the
first 128 of these  bitstrings; Unicode is an extension that  defines up to 2^16
two-byte characters, allowing encoding of virtually all written languages in the
world.

# What is a “word”?

4 consecutive bytes of computer storage (i.e. 32 bits).

# What is a “double word”?

8 consecutive bytes (64 bits).

##
# ?

A rough presentation  of floating-point arithmetic requires only a  few words: a
number `x`  is represented in  radix `β`  floating-point arithmetic with  a sign
`s`, a significand `m` (mantissa), and an exponent `e`, such that:

    x = s × m × β^e

---

A radix-β, precision-p, floating-point number is a number of the form:

    ±m₀.m₁m₂···mₚ₋₁ × β^e

where  the  expnonent  `e`  is  an integer,  and  `m₀.m₁m₂···mₚ₋₁`,  called  the
significand,  is   represented  in   radix  `β`,   and  verifies   the  relation
`|m₀.m₁m₂···mₚ₋₁| < β`.

---

A floating-point format is characterized by four integers:

   - a radix `β ≥ 2`

   - a precision `p ≥ 2`

     Roughly  speaking,  `p`  is  the  number of  “significant  digits”  of  the
     representation.

   - two extremal exponents `eₘᵢₙ` and `eₘₐₓ` such that `eₘᵢₙ < eₘₐₓ`

     In all practical cases,  `eₘᵢₙ < 0 < eₘₐₓ`, and  with all formats specified
     by the IEEE 754 standard, `eₘᵢₙ = 1 − eₘₐₓ`.

A finite floating-point number in such a format is a number `x` for which
there exists at least one representation (M, e) such that

    x = M · β^(e−p+1)

where:

   - `M` is an integer such that `|M| ≤ β^p − 1`, called the integral
     significand of the representation of `x`

   - `e` is an integer such that `eₘᵢₙ ≤ e ≤ eₘₐₓ`, called the exponent of the
     representation of `x`.

##
# Resources

<http://www.cs.nyu.edu/cs/faculty/overton/book/>

Refer to this  page for corrections to  the text, to download  programs from the
book, and to link to the web  pages mentioned in the bibliography, which will be
updated as necessary.

