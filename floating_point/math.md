# What does it mean for a set to be “countable”?

Intuitively:

You can count/enumerate its  elements from one of them to any  other in a finite
amount of time (this definition implies/needs the existence of an order).

The set of real numbers, for example, is UNcountable because you can't enumerate
all the numbers from 0 to 1 in a finite amount of time.
There are more  real numbers between 0 and  1, than in the whole  set of natural
numbers.

---

More formally:

There exists a one-to-one correspondence between this set and the set of natural
numbers; IOW, there exists a method which:

   - can enumerate all of its elements

        s₁, s₂, s₃, ...

   - doesn't contain any infinity  in the middle, so that  you can reach any
     element  in a finite amount of time

For example, this enumeration of the natural numbers proves that the set is countable:

    1 3 2 5 4 7 6 ...
                  ^^^
                  allowed

But not this one:

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
It follows that all of its elements can be written as an exhaustive enumeration:

    s₁, s₂, s₃, ...

For example, the start of the enumeration could look like this:

    ┌─────┬───────────────────┐
    │ s1  │ .5032164223981... │
    ├─────┼───────────────────┤
    │ s2  │ .9999261457682... │
    ├─────┼───────────────────┤
    │ s3  │ .0001042507334... │
    ├─────┼───────────────────┤
    │ ... │ ...               │
    └─────┴───────────────────┘

Now, let's build an element `s` by selecting the first decimal in `s₁` plus 1:

    5+1 = 6
    s = .6

then the second decimal of `s₂` minus 1:

    9-1 = 8
    s = .68

then the third decimal of `s₃` plus 1:

    0 + 1 = 1
    s = .681

Repeat the process  indefinitely, by extracting the `ᵢ`th decimal  of `sᵢ`, `+1`
if it's lower than 8, and `-1` if the decimal is 9.

Now, let's  compare the real  number `s` you've just  built with the  123th real
number in your enumeration.
You don't  know what the  latter looks  like, but you  *do* know that  its 123th
decimal is different than the one of `s`.
So, `s` is different than the 123th real number.
For the  same kind  of reason,  `s` is different  than any  real number  in your
enumeration.

But since `s` is a real number, it should be somewhere in the exhaustive enumeration.
This contradiction  implies that the  original assumption  is false: the  set of
real numbers is *not* countable.

##
# Express euler's number as the sum of an infinite series.  (2)

    e = Σ(1/n!), n ≥ 0

    e = Σ(1 + 1/n)^n, n ≥ 1

Note that any irrational number can be expressed as the sum of an infinite series.

#
# What's the value of
## `1 + a + a^2 + ... + a^n`?

Let's call this sum S.

    (1): a × S =      a + a^2 + a^3 + ... + a^n + a^(n+1)
    (2):   — S = —1 — a — a^2 — ...       — a^n

    (1) ∧ (2) ⇒   a × S — S = a^(n+1) — 1
              ⇔ (a — 1) × S = a^(n+1) — 1

              ⇔ S = a^(n+1) — 1
                    ───────────
                       a — 1

## `a^n + a^(n+1) + ... + a^m`?

Let's call this sum S.

    (1): a × S =        a^(n+1) + a^(n+2) + ... + a^m + a^(m+1)
    (2):   — S = —a^n — a^(n+1) — ...           — a^m

    (1) ∧ (2) ⇒   a × S — S = a^(m+1) — a^n
              ⇔ (a — 1) × S = a^(m+1) — a^n

              ⇔ S = a^(m+1) — a^n
                    ─────────────
                       a — 1

#
# Significant digits
## What are the four cases to consider when determining the significant digits in a number?

The number can be:

   - a value known to be exact (e.g. π)
   - a measured quantity
   - a quantity calculated by an addition/subtraction
   - a quantity calculated by a multiplication/division

##
## What does it mean for a digit in a measured quantity to be significant?

It  means  it's necessary  to  express  the  number  within the  uncertainty  of
measurement.

Ex:
        ┌ measured quantity
        ├───────────┐
        1.230 ± 0.002
        ├───┘
        └ 4 significant digits

Here, you need 4 digits to express the quantity within the uncertainty of measurement:

    1.228 ≤ x ≤ 1.232

<http://mathworld.wolfram.com/SignificantDigits.html>

### When is it *in*significant?

Only 0 can be insignificant, and only in one of two conditions.
Either it's a leading 0, or:

   - it's a trailing 0
   - the number has no radix point
   - we know from the context that the 0 can't be significant

     Example: we've measured the following quantity:

         q = 1300 ± 10

     The first  0 in 1300 is  significant because it's above  the uncertainty of
     measurement, but not the second 0.

---

All other digits are significant:

   - non-zero digits (1-9)
   - a 0 between two non-zero digits (e.g. 102)
   - a trailing 0 in a number with a radix point (e.g. 1.230)

<https://en.wikipedia.org/wiki/Significant_figures#Concise_rules>

##
### Is one of the 0 significant in 0.01?

No.
Even the 0 after the decimal point is not significant.

### In the absence of any context, where's the last significant digit in the measured quantity 1300?

    1300
      ^
      significant up to the hundreds

#### How to manually change this position?  (3)

Use an overline, the scientific notation, or a trailing dot.

---

Suppose you want to express that 1300 has only 2 significant digits.
You could write either of these:

    13̅00
    1.3 × 10^3

For 3 significant digits:

    130̅0
    1.30 × 10^3

For 4 significant digits:

        ┌ all digits are significant
        │
    1300.
    1300̅
    1.300 × 10^3

##
## What are the six types of values known to be exact?

  - integer counts (e.g. the number of oranges in a bag)
  - definitions of one unit in terms of another (e.g. a minute is 60 seconds)
  - actual prices asked or offered, and quantities given in requirement
    specifications
  - legally defined conversions, such as international currency exchange
  - scalar operations, such as "tripling" or "halving"
  - mathematical constants, such as π and e

### Which influence do they have on the significant digits of a calculated quantity?

None.

You must ignore them.

### Is the Avogadro's number a value known to be exact?

No, because it's known to us only by measurement.

### Is the speed of light a value known to be exact?

Yes, because its value is given by its definition.

##
## How many significant digits should there be in a quantity calculated by a multiplication/division?

As many as the measured quantity with the smallest amount of significant digits.

<https://en.wikipedia.org/wiki/Significant_figures#Arithmetic>
<https://en.wikipedia.org/wiki/Significance_arithmetic>

## What's the quantity calculated by
### `8 × 8`?

    ≈ 6 × 10^1

<https://en.wikipedia.org/wiki/Significance_arithmetic>

### `8 × 8.0`?

    ≈ 6 × 10^1

### `8.0 × 8.0`?

    ≈ 6.4 × 10^1

### `8.02 × 8.02`?

    ≈ 6.43 × 10^2

### `8 / 2.0`?

    ≈ 4

### `8.6 / 2.0012`?

    ≈ 4.3

### `2 × 0.8`?

    ≈ 2

###
## Where is the last significant digit in a quantity calculated by an addition/subtraction?

In the place  of the least significant  digit in the most  uncertain (i.e. least
accurate) of the numbers being summed.

## What's the quantity calculated by
### `1 + 1.1`?

    ≈ 2

1 and 1.1 are significant resp. up to the ones and tenths place.
Of  the two,  the  least accurate  is  the ones  place, so  the  result must  be
significant up to ones place.

### `1.0 + 1.1`?

    = 2.1

### `100 + 110`?

    ≈ 200

100 and 110 are significant resp. up to the hundreds place and tens place.
The result must be significant up to the hundreds place.

### `100. + 110.`?

    = 210.

### `1 × 10^2 + 1.1 × 10^2`?

    ≈ 2 × 10^2

`1 × 10^2` and `1.1 × 10^2` are significant resp. up to the hundreds and tens place.
The result must be significant up to the hundreds place.

### `1.0 × 10^2 + 111`?

    ≈ 2.1 × 10^2

### `123.25 + 46.0 + 86.26`?

    ≈ 255.5

### `100 — 1`?

    ≈ 100

