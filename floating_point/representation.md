# Number Systems
## What does the Roman number system require?  (3)

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
## Why is our current number system called positional?

The interpretation of a symbol depends on its position.

## What does a positional notation require?

The invention of the number 0, and the attribution of a symbol to it.
Zero is needed, for example, to distinguish 1 from 10.

## What other positional number system do you know and use on a daily basis?

The base 60 system used by the Babylonians.

We use it today in our division of  the hour into 60 minutes and the minute into
60 seconds.

##
# Symbols
## Which bitstrings can be abbreviated with
### the octal symbols 0 through 7?

Any bitstring  whose length  is 3 (because  `2^3 = 8`),  that is  the bitstrings
`000` through `111`.

### the hexadecimal symbols 0 through F abbreviate?

Any bitstring  whose length is  4 (because `2^3 =  16`), that is  the bitstrings
`0000` through `1111`.

###
# Negative Integers
## How much memory is usually used to store an integer?

With a 32-bit computer word.

##
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
To get the latter, you simply need to add the number whose representation is the
one of `x` after flipping all the bits.

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

##
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

The bit  in the  leftmost position  of the sum  cannot be  stored in  the 32-bit
computer word, and thus is discarded.
The result is 0, which is exactly what we want for `71 + (-71)`.

<https://en.wikipedia.org/wiki/Two%27s_complement>
<https://en.wikipedia.org/wiki/Method_of_complements>

---

Why did we choose the range `1 ≤  x  ≤ 2^31` for the negative integers?

Theory: A computer word can generate `2^32` bitstrings.
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
## Using an 8-bit format
### what's the binary representation of -1, -10 and -100 in 2's complement?

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

#### How to get back the numbers from these representations?

Compute its expansion as usual, but multiply the leftmost term with -1 instead of 1:

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
### show how the computer calculates
#### `50 + (—100)`?

     50  = (00110010)₂
     100 = (01100100)₂
    -100 = (10011100)₂    after flipping all the bits: 10011011
                          after adding 1:              10011100

    50 + (—100)
    =
      (00110010)₂
    + (10011100)₂
    ------------
      (11001110)₂

Check the result:

       v            v
      (11001110)₂ = —2^7 + 2^6 + 2^3 + 2^2 + 2^1
                  = —50

#### `100 + (—50)`?

    100 = (01100100)₂
    50  = (00110010)₂
    -50 = (11001110)₂

    100 + (—50)
    =
      (01100100)₂
    + (11001110)₂
    ------------
      (00110010)₂

#### `50 + 50`?

    50 = (00110010)₂

    50 + 50
    =
      (00110010)₂
    + (00110010)₂
    ------------
      (01100100)₂
         ^
         the previous column carries a 1 (1 + 1 = 10),
         so when you reach this one, you have to sum three 1s: 1 + 1 + 1

                (1 + 1 + 1)₂ = (10 + 1)₂ = (11)₂

         you must deal with that sum by writing a 1 in the column
         and carry another 1 in the next column

##
# Floating-point numbers
## What's the scientific notation of a number `x`?

    ± S × 10^E

`S` is called the significand, and `E` the exponent.

### What's its normalized form?

    ± S × 10^E
    1 ≤ S < 10

##
## What's the floating-point representation?

The usage  of the  concept of  scientific notation,  in a  binary implementation
context, to represent numbers in computer memory.

    ± S × 2^E
    1 ≤ S < 2

### Why is it called “floating”-point?

During the normalization of the representation,  you can imagine that the binary
point floats to the position immediately after the first non-zero digit.

    x = 123.456
      = (1111011.0111010010)₂ × 2^0
      = (1.1110110111010010)₂ × 2^6
          ^     ^
          new   old position

---

> The term floating point refers to the  fact that a number's radix point (decimal
> point, or,  more commonly in computers,  binary point) can "float";  that is, it
> can be placed anywhere relative to the significant digits of the number.

Source: <https://en.wikipedia.org/wiki/Floating-point_arithmetic>

##
## What's a computer number format?

The internal representation of numeric values in digital computer.

The encoding between numerical values and bit patterns is chosen for convenience
of the operation of the computer.
Different types  of processors  may have  different internal  representations of
numerical values.

##
## How is a number stored in the fixed-point format?

Its computer word(s) is/are divided into three fields:

   - a 1-bit field for the sign of the number
   - a field of bits for the binary representation of the number before the binary point
   - a field of bits for the binary representation after the binary point

For example, in a 32-bit word with field  widths of 15 and 16, resp., the number
11/2 would be stored as:

    ┌───┬─────────────────┬──────────────────┐
    │ 0 │ 000000000000101 │ 1000000000000000 │
    └───┴─────────────────┴──────────────────┘

While the number 1/10 would be approximately stored as:

    ┌───┬─────────────────┬──────────────────┐
    │ 0 │ 000000000000000 │ 0001100110011001 │
    └───┴─────────────────┴──────────────────┘

### Why is this format rarely used?

It's too limited by the size of the numbers it can store.
In the  previous example, only numbers  ranging in size from  (exactly) 2^-16 to
(slightly less than) 2^15 could be stored.
This is not adequate for many applications.

##
## How is a number stored in a floating-point format?

Its computer word(s) is/are divided into three fields:

   - a 1-bit field for the sign of the number (0 = positive, 1 = negative)
   - a field of bits for the binary representation of the exponent
   - a field of bits for the binary representation of the fractional part

### What's a floating-point number?

A  real number  which can  be stored  *exactly* (no  rounding required)  using a
floating-point format.

#### If a real is not a floating-point number, how is it stored?

It's rounded first.

##
### What's the value of the first bit of the binary representation of the significand?

No matter the number, it's always 1.

#### Why is it called a hidden bit?

Because it's not stored since it doesn't need to be.

###
### What's the name of the bits following the binary point?  (2)

The fractional part (of the significand), also called the fraction field.

###
### What are the names (new and old) of the three main floating-point formats?

    ┌─────────────────────┬────────────────────┐
    │ IEEE 754-1985 name  │ IEEE 754-2008 name │
    ├─────────────────────┼────────────────────┤
    │ single-precision    │ binary32           │
    ├─────────────────────┼────────────────────┤
    │ double-precision    │ binary64           │
    ├─────────────────────┼────────────────────┤
    │ quadruple-precision │ binary128          │
    └─────────────────────┴────────────────────┘

#### What are the two differences between them?

The size of the exponent field, and significand field.

###
### What's the width of the exponent field in the
#### single-precision floating-point format?

8

#### double-precision floating-point format?

11

#### quadruple-precision floating-point format?

15

###
### What's the exponent bias?

An integer  number added  to the  exponent of a  floating-point number  when the
latter must be stored in memory.

<https://en.wikipedia.org/wiki/Exponent_bias>

#### Why is it necessary?

Exponents are signed values, but two's complement – the usual representation for
signed values – would make comparison harder.

#### How is it computed?

    2^(k-1) — 1

`k` is the size in bits of  the exponent field; that is 8 (single-precision), 11
(double-precision) or 15 (quadruple-precision).

Thus, its value is one of:

    2^(8-1) — 1  = 127
    2^(11-1) — 1 = 2047
    2^(15-1) — 1 = 32767

#### How is it used?

The exponent  is stored as an  unsigned value suitable for  comparison, and when
being interpreted, it's converted back into an exponent within a signed range by
subtracting the bias.

---

Here's what the computer would do to compare the exponents `100` and `101`:

    100 + bias = (01100100)₂
               + (01111111)₂
               -------------
                 (11100011)₂

    101 + bias = (01100101)₂
               + (01111111)₂
               -------------
                 (11100100)₂

Both representations are identical until the sixth bit, where the representation
of 101 contains a 1 while the representation of 100 contains a 0.
So, the computer would conclude that the exponent 101 is bigger than the exponent 100.

---

Here's what the computer would do to compare the exponents `-100` and `-101`:

    -100 + bias = (10011100)₂
                + (01111111)₂
                -------------
                 (100011011)₂

    -101 + bias = (10011011)₂
                + (01111111)₂
                -------------
                 (100011010)₂

Both representations are identical until  the last bit, where the representation
of -100 contains a 1 while the representation of -101 contains a 0.
So,  the computer  would conclude  that  the exponent  -100 is  bigger than  the
exponent -101.

#### What is the range of possible stored values for the exponent of a single-precision floating-point number?

The exponent is stored in the range `[0,255]`.

##### What about the range of possible interpreted values?

A stored exponent is  interpreted by subtracting the bias – which  is 127 for an
8-bit exponent – to get an exponent value in the range `[-127,128]`.

The same thing applies to a double-precision / quadruple-precision number:

    ┌─────────────────────┬─────────────┬──────────────┬───────────────────┐
    │ number format       │ field width │ stored value │ interpreted value │
    ├─────────────────────┼─────────────┼──────────────┼───────────────────┤
    │ single-precision    │ 8           │ 0..255       │ -127..128         │
    ├─────────────────────┼─────────────┼──────────────┼───────────────────┤
    │ double-precision    │ 11          │ 0..2047      │ -1023..1024       │
    ├─────────────────────┼─────────────┼──────────────┼───────────────────┤
    │ quadruple-precision │ 15          │ 0..32767     │ -16383..16384     │
    └─────────────────────┴─────────────┴──────────────┴───────────────────┘

##### What are the two values which are processed specially?

The stored values full of 0s and  full of 1s (e.g. 0 and 255 in single-precision
format).

##
### What's the single-precision format floating-point representation for
#### 11/2?

    11/2 = (101.1)₂ = (1.011)₂ × 2^2

    ┌───┬──────────┬─────────────────────────┐
    │ 0 │ 10000001 │ 01100000000000000000000 │
    └───┴──────────┴─────────────────────────┘

Notice that:

   - the exponent is `2+127`
   - the fraction field doesn't contain the initial `1`; it's hidden.

#### 71?

    71 = (1000111)₂ = (1.000111)₂ × 2^6

    ┌───┬──────────┬─────────────────────────┐
    │ 0 │ 10000101 │ 00011100000000000000000 │
    └───┴──────────┴─────────────────────────┘

`10000101` is the stored exponent 133 (127 + 6).

#### 1?

    1 = (1)₂ = (1.0)₂ × 2^0

    ┌───┬──────────┬─────────────────────────┐
    │ 0 │ 01111111 │ 00000000000000000000000 │
    └───┴──────────┴─────────────────────────┘

#### 2^71?

    2^71 = (1.0) × 2^71

    ┌───┬──────────┬─────────────────────────┐
    │ 0 │ 11000110 │ 00000000000000000000000 │
    └───┴──────────┴─────────────────────────┘

###
### In single-precision format, what's the
#### largest floating-point number?

      (1.11111111111111111111111)₂ × 2^127

    =  (2^-23 + 2^-22 + ... + 2^0) × 2^127

    =  2^(0+1) — 2^-23  × 2^127
       ───────────────
             2 — 1

    =  (2 — 2^-23) × 2^127

    =  2^128 — 2^104

Note that we can't use the exponent 128, because it's interpreted specially.

#### smallest positive floating-point number?

    (1.00000000000000000000000)₂ × 2^-126
    =
    2^-126

Note that we can't use the exponent -127, because it's interpreted specially.

#### smallest positive **integer** that is not exactly representable?

There are two reasons which could explain why an integer is not exactly representable:

   - the exponent is too big (> 126)
   - the significand has too many digits (> 23)

Since we're  looking for the  smallest integer, and  the significand has  a much
lesser impact on the magnitude of a  number compared to the exponent, we need to
find the smaller integer whose significand contains 24 digits; that is:

    1.000000000000000000000000 × 2^24
    =
    2^24
    =
    16777216

---

You could think the answer is 2^23, because the latter needs 24 digits (a 1 then 24 0s).
But you  would be wrong,  because in a floating-point  number, the first  bit is
hidden; i.e. the computer assumes it's 1.
So, the computer would only need 23 bits to store the significand of 2^23, and not 24.

##
# Resources

<http://www.cs.nyu.edu/cs/faculty/overton/book/>

Refer to this  page for corrections to  the text, to download  programs from the
book, and to link to the web  pages mentioned in the bibliography, which will be
updated as necessary.

###
##
##
# TODO
## ?

Exercise 3.11

Suppose we change our system from:

    x = ±S × 2^E, 1 ≤ S < 2
    S = (b₀.b₁b₂b₃...b₂₃)₂, b₀ = 1
    -128 ≤ E ≤ 127

to:

    x = ±S × 2^E, 1/2 ≤ S < 1
    S = (0.b₁b₂b₃...b₂₄)₂, b₁ = 1
    -128 ≤ E ≤ 127

That is, suppose the magnitue of the significand is halved.

---

What is the new largest floating-point number?

    (0.111111111111111111111111)₂ × 2^127
    =
    (2^-1 + 2^-2 + ... + 2^-24) × 2^127
    =
    (2^-24 + 2^-23 + ... + 2^-1) × 2^127
    =
    (2^(-1 + 1) — 2^-24) × 2^127
    =
    2^127 — 2^103

Notice that it's half the old value:

    2^127 — 2^103

    = 1/2 × (2^128 — 2^104)

---

What is the new smallest positive floating-point number?

    (0.100000000000000000000000)₂ × 2^-128
    =
    2^-129

Notice that it's half the old value:

    2^-129 = 1/2 × 2^-128

---

What is the new smallest positive integer that is not exactly representable as a floating-point number?

    (0.1000000000000000000000000)₂ × 2^25
    =
    2^24
    =
    16777216

Notice that it's the same as the old value.

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
On  the other  hand, if  two  integers with  opposite sign  are added  together,
integer overflow cannot  occur, although an overflow bit may  arise when the 2's
complement bitstrings are added together.
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
     representation of `x`

