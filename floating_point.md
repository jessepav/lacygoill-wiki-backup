# Terminology
## Where does the word “bit” come from?

It's an abbreviation for binary digit.

### How can I view it physically?

As a single physical entity in one of two states: on or off.

##
## How do you call a string of bits?

A bitstring.

## What can a byte represent?

Up to 256 bitstrings, which may be viewed as representing the integers from 0 to
255, or some characters.

The ASCII  encoding scheme  defines standard  character interpretations  for the
first 128 of these bitstrings.

##
## What is a “word”?

4 consecutive bytes of computer storage (i.e. 32 bits).

## What is a “double word”?

8 consecutive bytes (64 bits).

###
## What's the representation of a number?

The sequence of symbols which expresses this number in a given base.

For example, the representation of seventy one  is `71` in base 10, and `1000111`
in base 2.

## What's the expansion of a number?

A sum of powers of the base, each  power being multiplied by one of the digit of
the number:

    (71)₁₀ = 7 × 10 + 1
             ├────────┘
             └ expansion of 71 in base 10

    (1000111)₂ = 1 × 64 + 0 × 32 + 0 × 16 + 0 × 8 + 1 × 4 + 1 × 2 + 1 × 1
                 ├──────────────────────────────────────────────────────┘
                 └ expansion of 71 in base 2

## What's the difference between a decimal point, a binary point, and a radix point?

They stand for the same thing, but they're used in different contexts.


    ┌───────────────┬────────────────────────────────┐
    │               │ applies to a representation in │
    ├───────────────┼────────────────────────────────┤
    │ decimal point │ decimal                        │
    ├───────────────┼────────────────────────────────┤
    │ binary point  │ binary                         │
    ├───────────────┼────────────────────────────────┤
    │ radix point   │ arbitrary base                 │
    └───────────────┴────────────────────────────────┘

###
## How do you qualify the representation of a nonintegral real number
### which is not finite?

It's said to be “nonterminating”.

### whose symbols after the decimal/binary point repeat periodically?

It's said to be “repeating”.

###
## Give an example of number whose representation is finite in decimal, but not in binary.

0.1

In decimal, there's only one digit after the decimal point.
In binary, there's an infinite number of bits after the binary point:

    1/10 = (0.0001100110011...)₂ = 1/16 + 1/32 + 0/64 + 0/128 + 1/256 + 1/512 + 0/1024 + ...
            ├────────────────┘
            └ mnemonic: 0.0 then 0011, 0011, ...

###
## Which property is shared by
### all rational numbers?

Their representation is always either finite or repeating.

    1/7 = (0.142857142857)₁₀
             ├────┘├────┘
             │     └ period 2
             └ period 1

### all irrational numbers?

Their representation is neither finite nor repeating.

    √2 = (1.414213...)₁₀
    π  = (3.141592...)₁₀
    e  = (2.71828182845...)₁₀

##
## What's “integer overflow”?

Integer  overflow  occurs when  two  positive  or  negative integers  are  added
together, and the result gives an integer `≥ 2^31` or `< -2^31`.

## If the result of an operation involving 32-bit words contains more than 32 bits, how are the excessive bits called?

Overflow bits.

### What happens to them?

They're discarded.

##
## What's the meaning of the acronym IEEE?

Institute for Electrical and Electronics Engineers.

### How is it pronounced?

“I triple E.”

##
# A Bit Of Math
## What does it mean for a set to be “countable”?

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

## How to prove that
### the set of rational numbers is countable?

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

### the set of real numbers is UNcountable?

Use the Cantor's diagonal argument:
<https://en.wikipedia.org/wiki/Cantor%27s_diagonal_argument>

Let's assume that the set of real numbers is countable.
It follows that all of its elements can be written as an exhaustive enumeration:

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

###
## Express euler's number as the sum of an infinite series.  (2)

    e = Σ(1/n!), n ≥ 0

    e = Σ(1 + 1/n)^n, n ≥ 1

Note that any irrational number can be expressed as the sum of an infinite series.

## What's the value of `1 + a + a^2 + ... + a^n`?

Let's call this sum S.

    (1): a × S =      a + a^2 + a^3 + ... + a^n + a^(n+1)
    (2):   — S = —1 — a — a^2 — ...       — a^n

    (1) ∧ (2) ⇒   a × S — S = a^(n+1) — 1
              ⇔ (a — 1) × S = a^(n+1) — 1

              ⇔ S = a^(n+1) — 1
                    ───────────
                       a — 1

## What's the value of `a^n + a^(n+1) + ... + a^m`?

Let's call this sum S.

    (1): a × S =        a^(n+1) + a^(n+2) + ... + a^m + a^(m+1)
    (2):   — S = —a^n — a^(n+1) — ...           — a^m

    (1) ∧ (2) ⇒   a × S — S = a^(m+1) — a^n
              ⇔ (a — 1) × S = a^(m+1) — a^n

              ⇔ S = a^(m+1) — a^n
                    ─────────────
                       a — 1

##
# Numeric Systems
## What does the Roman numeric system require?  (3)

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

### What was such a system well-suited for?

Easy transcription of numbers to an abacus for calculation.

### What was such a system *not* well-suited for?  (2)

Calculation with pencil and paper:

       CXXIII
    + CCCCLVI
    ---------
    = ???????

Representation of large numbers.

###
## Why is our current numeric system called positional?

The interpretation of a symbol depends on its position.

## What does a positional notation require?

The invention of the number 0, and the attribution of a symbol to it.
Zero is needed, for example, to distinguish 1 from 10.

## What other positional numeric system do you know and use on a daily basis?

The base 60 system used by the Babylonians.

We use it today in our division of  the hour into 60 minutes and the minute into
60 seconds.

##
# Representations
## Which bitstrings can be abbreviated with
### the octal symbols 0 through 7?

Any bitstring  whose length  is 3 (because  `2^3 = 8`),  that is  the bitstrings
`000` through `111`.

### the hexadecimal symbols 0 through F abbreviate?

Any bitstring  whose length is  4 (because `2^3 =  16`), that is  the bitstrings
`0000` through `1111`.

###
## What's the binary representation of `2^n`?

A 1 followed by `n` 0s.

Note that this means that the representation of `2^n` contains `n+1` bits.

## If I know the binary representation of the positive integer `x`, how do I get the representation of `2^32 — x`?

Flip all the bits and add 1.

---

For example, the representation of 71 is:

    00000000000000000000000001000111

Once you flip all the bits, you get:

    11111111111111111111111110111000

And if you add 1, you get:

    11111111111111111111111110111001
                                   ^

which is the representation of `2^32 — 71`.

---

Here's an intuitive reasoning to find this method:

You know the representation of `x`, and you're looking for the one of `2^32 — x`.
Let's call this number `y`.
Which  relationship  do  you  know  about  `y`,  involving  only  numbers  whose
representations are known to you?

    x + y = 2^32
    │       ├──┘
    │       └ you know its representation, because it's simple
    └ you know its representation, by hypothesis

So, you're looking for sth which, when added to `x`, gives a 1 followed by 32 0s.

You don't know how to get that, but you know how to get sth close: 32 1s.
Add the number whose representation is the one of `x` after flipping all the bits.

Now, to get from 32 1s to a one and 32 0s, all you need is add 1.
Similarly, to get from 999 to 1000, all you need is add 1.

---

Proof:

Let's call `y` the representation of `x` after all the bits have been flipped.
The representation of the sum `x + y` is:

    11111111111111111111111111111111

This matches the expansion:

    2^0 + 2^1 + 2^2 + ... + 2^31
    =
    2^32 - 1

Which implies that:

    x + y = 2^32 - 1
    ⇒
    2^32 - x = y + 1

The last  equality tells  us that  the binary  representation of  `2^32 —  x` is
obtained after flipping  all the bits of `x`  – because of `y` in the  rhs – and
adding 1.

###
## How much memory is usually used to store an integer?

With a 32 bit word.

## Which representation is usually used to store a negative integer?

Most machines use a representation called 2's complement.

With this representation, positive integers are stored as usual.
However, a negative integer `—x`, where `1 ≤  x ≤ 2^31`, is stored as the binary
representation of the positive integer `2^32 — x`.

For example, the integer -71 is stored as:

    11111111111111111111111110111001

And the sum of 71 and -71 is:

      ( 00000000000000000000000001000111 )₂
    + ( 11111111111111111111111110111001 )₂
    = (100000000000000000000000000000000 )₂
       ^
       overflow bit

The bit in the leftmost position of the sum cannot be stored in the 32-bit word,
and thus is discarded.
The result is 0, which is exactly what we want for `71 + (-71)`.

<https://en.wikipedia.org/wiki/Two%27s_complement>
<https://en.wikipedia.org/wiki/Method_of_complements>

---

Why did we choose the range `1 ≤  x  ≤ 2^31` for the negative integers?

Theory: A word can generate `2^32` bitstrings.
0 consumes one of them, so there're  `2^32 — 1` bitstrings left for the negative
and positive integers.
This is not divisible  by two, so we have to choose how  many bitstrings to give
to the positive integers: either `2^31` or `2^31 — 1`.
If we give `2^31`, the representations  of all positive integers will begin with
a 0, except:

    10000000000000000000000000000000

And any  representation beginning  with a  1 will stand  for a  negative number,
except the one mentioned just above.

These exceptions may cause  some issues, or just seem awkward,  so it was chosen
to give only `2^31 — 1` bitstrings to the positive integers.

### Which naive alternative machines could use?

The most obvious idea  is sign-and-modulus: use one of the  32 bits to represent
the sign, and use  the remaining 31 bits to store the  magnitude of the integer,
which may then range from 0 to `2^31 — 1`.

#### Why don't they use it?  (3)

The 2's complement method provides three benefits:

   - the addition of a negative number represented by the sign-and-modulus
     method is more complicated, because you have to process the first bit
     specially

   - with the sign-and-modulus method, there are two zeros (+0 and -0)

     Every application will need to take  extra steps to make sure that non-zero
     values are also not negative zero.

   - extending the width of the register where the negative number is being
     stored is easier

     Compare:

            1110 (negative two, in four bits, using the 2's complement method)
        11111110 (negative two, in eight bits, using the 2's complement method)

     To go from `1110`  to `11111110`, all the computer has to  do is repeat the
     most significant bit: that requires 4 operations.

            1010 (negative two, in four bits, using the sign-and-modulus method)
        10000010 (negative two, in eight bits, using the sign-and-modulus method)

     This time,  to go from  `1010` to `10000010`,  the computer *first*  has to
     clear the most  significant bit:

            1010
            ↓
            0010

     Then it can  repeat 0, until the last  bit where it puts a 1  for the sign:
     that requires 5 operations.

     The clearing of  the most significant bit is an  extra operation, for which
     there's no equivalent in the 2's complement method.

<https://stackoverflow.com/a/1125317/9780968>

###
## What's the binary representation of -1, -10 and -100?

    ┌──────┬──────────┐
    │ -1   │ 11111111 │
    ├──────┼──────────┤
    │ -10  │ 11110110 │
    ├──────┼──────────┤
    │ -100 │ 10011100 │
    └──────┴──────────┘

Proof:

    1
    ↓     binary representation
    00000001
    ↓     flip the bits
    11111110
    ↓     add 1
    11111111

    10
    ↓
    00001010
    ↓
    11110101
    ↓
    11110110

    100
    ↓
    01100100
    ↓
    10011011
    ↓
    10011100

### How can you check these representations?

Compute their expansion, but multiply the leftmost term with -1 instead of 1:

                  v
    (11111111)₂ = -2^7 + 2^6 + 2^5 + 2^4 + 2^3 + 2^2 + 2^1 + 2^0
                = -128 + 64 + 32 + 16 + 8 + 4 + 2 + 1
                = -1

    (11110110)₂ = -2^7 + 2^6 + 2^5 + 2^4 + 2^2 + 2^1
                = -128 + 64 + 32 + 16 + 4 + 2
                = -10

    (10011100)₂ = -2^7 + 2^4 + 2^3 + 2^2
                = -128 + 16 + 8 + 4
                = -100

##
## ?

Integrate here our comments from `vim-math` regarding significant digits.

## ?

All computers provide hardware instructions for adding integers.
If two  positive integers  are added  together, the result  may give  an integer
greater than or equal to `2^31`.
In this case, we say that integer overflow occurs.
One would hope that this leads to an informative error message for the user, but
whether or  not this happens  depends on  the programming language  and compiler
being used.
In some  cases, the overflow  bits may be discarded  and the programmer  must be
alert to prevent this from happening.
The same problem may occur if two negative integers are added together, giving a
negative integer with magnitude greater than `2^31`.
On the other  hand, although an overflow  bit may arise when  the 2's complement
bitstrings are added together.
Consider the operation:

    x + (—y)

where

    0 ≤ x ≤ 2^31 — 1
    1 ≤ y ≤ 2^31

Clearly, it  is possible  to store the  desired result `x  — y`  without integer
overflow.
The result may be positive, negative, or  zero, depending on whether `x > y`, `x = y`,
or `x < y`.

Now let us see what happens if we add the 2's complement representations for `x`
and `—y`, i.e., the bitstrings for the non-negative numbers `x` and `2^32 — y`.
We obtain the bitstring for:

    2^32 + x — y = 2^32 — (y — x)

If `x ≥ y`, the leftmost bit of  the result is an overflow bit, corresponding to
the power `2^32`, but this bit can  be discarded, giving the correct result `x — y`.
If `x <  y`, the result fits  in 32 bits with  no overflow bit, and  we have the
desired  result, since  it  represents the  negative  value `—(y  —  x)` in  2's
complement.

This demonstrates  an important  property of  2's complement  representation: no
special hardware is needed for integer subtraction.
The  addition hardware  can  be used  once  the negative  number  `—y` has  been
represented using 2's complement.

## ?

Show the details for the integer sums `50 + (—100)`, `100 + (—50)` and
`50 + 50`, using an 8-bit format.

    50 + (-100)

    50:    110010
    100:  1100100

    -100: 0011100

    50-100:
           110010
        + 0011100
        ---------
          1001110

## ?

Exercise 3.8

What  is  the  largest  floating  point number  in  this  system,  assuming  the
significand field can store only the bits `b₁...b₂₃` and the exponent is limited
by `—128 ≤ E ≤ 127`?

      (1.11111111111111111111111)₂ × 2^127

    =  (2^0 + 2^-1 + ... + 2^-23)  × 2^127
    =  (2^-23 + 2^-22 + ... + 2^0) × 2^127

    =  2^(0+1) — 2^-23  × 2^127
       ───────────────
             2 — 1

    =  (2 — 2^-23) × 2^127

    =

    2^128 — 2^104

## ?

Exercise 3.9

What is the smallest positive floating point number in this system?

    (1.00000000000000000000000)₂ × 2^-128
    =
    2^-128

## ?

Exercise 3.10

What is the smallest positive **integer** that is not exactly representable as a
floating point number in this system?

Here are the binary representations of the first eight positive integers:

    ┌───┬──────┐
    │ 1 │ 1    │
    ├───┼──────┤
    │ 2 │ 10   │
    ├───┼──────┤
    │ 3 │ 11   │
    ├───┼──────┤
    │ 4 │ 100  │
    ├───┼──────┤
    │ 5 │ 101  │
    ├───┼──────┤
    │ 6 │ 110  │
    ├───┼──────┤
    │ 7 │ 111  │
    ├───┼──────┤
    │ 8 │ 1000 │
    └───┴──────┘

Here are the same representations but in floating point:

    ┌───┬─────────────┐
    │ 1 │ 1.0   × 2^0 │
    ├───┼─────────────┤
    │ 2 │ 1.0   × 2^1 │
    ├───┼─────────────┤
    │ 3 │ 1.1   × 2^1 │
    ├───┼─────────────┤
    │ 4 │ 1.00  × 2^2 │
    ├───┼─────────────┤
    │ 5 │ 1.01  × 2^2 │
    ├───┼─────────────┤
    │ 6 │ 1.10  × 2^2 │
    ├───┼─────────────┤
    │ 7 │ 1.11  × 2^2 │
    ├───┼─────────────┤
    │ 8 │ 1.000 × 2^3 │
    └───┴─────────────┘

Notice that  the exponent always  matches the number  of bits in  the fractional
part of the significand (except for the  special case), exactly like it would do
in decimal.

We could go on until this number:

    1.11111111111111111111111 × 2^23
    =
    111111111111111111111111

The integer afterwards is:

     111111111111111111111111 + 1
    =
    1000000000000000000000000

Its exact floating point representation is:

     1000000000000000000000000
    =
    1.000000000000000000000000 × 2^24

The fractional part  of its significand contains  24 bits which is  too much for
our system, which can only contain 23 bits.

So,  the smallest  positive  integer  that is  not  exactly  representable as  a
floating point number is 2^24, i.e. 16777216.

---

Another way of finding the solution:

Our system can only express numbers with 24 significant bits.
So, it can't express exactly any integer with 25 significant bits or more.
The smallest integer with 25 significant bits is:

    1000000000000000000000000
    =
    2^24

## ?

Exercise 3.11

Suppose we change so our system from:

    x = ±S × 2^E, 1 ≤ S < 2
    S = (b₀.b₁b₂b₃...b₂₃)₂, b₀ = 1
    -128 ≤ E ≤ 127

to:

    x = ±S × 2^E, 1/2 ≤ S < 1
    S = (0.b₁b₂b₃...b₂₄)₂, b₁ = 1
    -128 ≤ E ≤ 127

---

What is the new largest floating point number?

    0.111111111111111111111111 × 2^127
    =
    (2^-1 + 2^-2 + ... + 2^-24) × 2^127
    =
    (2^-24 + 2^-23 + ... + 2^-1) × 2^127
    =
    (2^(-1 + 1) — 2^-24) × 2^127
    =
    2^127 — 2^103

---

What is the new smallest positive floating point number?

    0.100000000000000000000000 × 2^-128
    =
    1.00000000000000000000000 × 2^-129
    =
    2^-129

---

What is the new smallest positive integer that is not exactly representable as a floating point number?

    0.1000000000000000000000000 × 2^25
    =
    2^24
    =
    16777216

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

