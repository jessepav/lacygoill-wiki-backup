# Symbols
## What can a byte represent?

Up to 256 bitstrings, which may be viewed as representing the integers from 0 to
255, or some characters.

The ASCII  encoding scheme  defines standard  character interpretations  for the
first 128 of these bitstrings.

##
## Which bitstrings can be abbreviated with
### the octal symbols 0 through 7?

Any bitstring  whose length  is 3 (because  `2^3 = 8`),  that is  the bitstrings
`000` through `111`.

### the hexadecimal symbols 0 through F abbreviate?

Any bitstring  whose length is  4 (because `2^3 =  16`), that is  the bitstrings
`0000` through `1111`.

##
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

###
## Give an example of number whose representation is finite in decimal, but not in binary.

0.1

In decimal, there's only one digit after the decimal point.
In binary, there's an infinite number of bits after the binary point:

    1/10 = (0.0001100110011...)₂ = 1/16 + 1/32 + 0/64 + 0/128 + 1/256 + 1/512 + 0/1024 + ...
            ├────────────────┘
            └ mnemonic: 0.0 then 0011, 0011, ...

##
# Numeral Systems
## On what does the Roman numeral system rely to work?  (3)

It uses a different **symbol for each power of 10**:

   - X for 10
   - C for 100
   - M for 1000
   - ...

It also uses **repetition** to indicate how many of each power of 10 is present.

Finally, it uses  additional symbols to **abbreviate a group  of 5 consecutive**
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
## Why is our current numeral system called positional?

The interpretation of a symbol depends on its position.

## What does a positional notation require?

The invention of the number 0, and the attribution of a symbol to it.
Zero is needed, for example, to distinguish 1 from 10.

## What other positional numeral system do you know and use on a daily basis?

The base 60 system used by the Babylonians.

We use it today in our division of  the hour into 60 minutes and the minute into
60 seconds.

##
# Negative Integers
## How much memory is usually used to store an integer?

With a 32-bit computer word.

##
## What's the binary representation of `2^n`?

A 1 followed by `n` 0s.

Note that this means that the representation of `2^n` contains `n+1` bits.

## If I know the binary representation of the positive integer `x`, how do I get the representation of `2^32 − x`?

Flip all the bits and add 1.

---

For example, the representation of 71 is:

    00000000000000000000000001000111

Once you flip all the bits, you get:

    11111111111111111111111110111000

And if you add 1, you get:

    11111111111111111111111110111001
                                   ^

which is the representation of `2^32 − 71`.

---

Here's an intuitive reasoning to find this method:

You know the representation of `x`, and you're looking for the one of `2^32 − x`.
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

Now, to get from 32 1s to a one and 32 0s, all you need is to add 1.
Similarly, to get from 999 to 1000, all you need is to add 1.

---

Proof:

Let's call `y` the representation of `x` after all the bits have been flipped.
The representation of the sum `x + y` is:

    11111111111111111111111111111111

This matches the expansion:

    2^0 + 2^1 + 2^2 + ... + 2^31
    =
    2^32 − 1

Which implies that:

    x + y = 2^32 − 1
    ⇒
    2^32 − x = y + 1

The last  equality tells  us that  the binary  representation of  `2^32 −  x` is
obtained after flipping  all the bits of `x`  – because of `y` in the  rhs – and
adding 1.

##
## Which representation is usually used to store a negative integer?

Most machines use a representation called 2's complement.

With this representation, positive integers are stored as usual.
However, a negative integer `-x`, where `1 ≤  x ≤ 2^31`, is stored as the binary
representation of the positive integer `2^32 − x`.

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

- <https://en.wikipedia.org/wiki/Two%27s_complement>
- <https://en.wikipedia.org/wiki/Method_of_complements>

---

Why did we choose the range `1 ≤  x  ≤ 2^31` for the negative integers?

Theory: A computer word can generate `2^32` bitstrings.
0 consumes one of them, so there're  `2^32 − 1` bitstrings left for the negative
and positive integers.
This is not divisible  by two, so we have to choose how  many bitstrings to give
to the positive integers: either `2^31` or `2^31 − 1`.
If we give `2^31`, the representations  of all positive integers will begin with
a 0, except:

    10000000000000000000000000000000

And any  representation beginning  with a  1 will stand  for a  negative number,
except the one mentioned just above.

These exceptions may cause  some issues, or just seem awkward,  so it was chosen
to give only `2^31 − 1` bitstrings to the positive integers.

### Which naive alternative could machines use?

The most obvious idea  is sign-and-modulus: use one of the  32 bits to represent
the sign, and use  the remaining 31 bits to store the  magnitude of the integer,
which may then range from 0 to `2^31 − 1`.

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
#### `50 + (-100)`?

     50  = (00110010)₂
     100 = (01100100)₂
    -100 = (10011100)₂    after flipping all the bits: 10011011
                          after adding 1:              10011100

    50 + (-100)
    =
      (00110010)₂
    + (10011100)₂
    ------------
      (11001110)₂

Check the result:

       v            v
      (11001110)₂ = -2^7 + 2^6 + 2^3 + 2^2 + 2^1
                  = -50

#### `100 + (-50)`?

    100 = (01100100)₂
    50  = (00110010)₂
    -50 = (11001110)₂

    100 + (-50)
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
## How is a number stored in a fixed-point system?

Its computer word(s) is/are divided into three fields:

   - a 1-bit field for the sign of the number
   - a field of bits for the binary representation of the number before the binary point
   - a field of bits for the binary representation after the binary point

For example, in a  32-bit word with field widths of 15 and  16 resp., the number
11/2 would be stored as:

    ┌───┬─────────────────┬──────────────────┐
    │ 0 │ 000000000000101 │ 1000000000000000 │
    └───┴─────────────────┴──────────────────┘

While the number 1/10 would be approximately stored as:

    ┌───┬─────────────────┬──────────────────┐
    │ 0 │ 000000000000000 │ 0001100110011001 │
    └───┴─────────────────┴──────────────────┘

### Why is this system rarely used?

It's too limited by the size of the numbers it can store.
In the  previous example, only numbers  ranging in size from  (exactly) 2^-16 to
(slightly less than) 2^15 could be stored.
This is not adequate for many applications.

##
## How is a number stored in a floating-point system?

Its computer word(s) is/are divided into three fields:

   - a 1-bit field for the sign of the number (0 = positive, 1 = negative)
   - a field of bits for the binary representation of the exponent
   - a field of bits for the binary representation of the fractional part

### What's a floating-point number?

A  real number  which can  be stored  *exactly* (no  rounding required)  using a
floating-point format.

#### If a real number is not a floating-point number, how is it stored?

It's rounded first.

##
## What are the names (new and old) of the three main floating-point formats?

    ┌─────────────────────┬────────────────────┐
    │ IEEE 754-1985 name  │ IEEE 754-2008 name │
    ├─────────────────────┼────────────────────┤
    │ single-precision    │ binary32           │
    ├─────────────────────┼────────────────────┤
    │ double-precision    │ binary64           │
    ├─────────────────────┼────────────────────┤
    │ quadruple-precision │ binary128          │
    └─────────────────────┴────────────────────┘

### What are the two differences between them?

The size of the exponent field, and significand field.

##
## What's the width of the exponent field in the
### single-precision floating-point format?

8

### double-precision floating-point format?

11

### quadruple-precision floating-point format?

15

##
## What's the range of possible stored values for the exponent of a single-precision floating-point number?

`[1,254]`

0 and 255 are interpreted specially.

### What about the range of possible interpreted values?

A stored exponent is  interpreted by subtracting the bias – which  is 127 for an
8-bit exponent – to get an exponent value in the range `[-127,128]`.

The same thing applies to a double-precision / quadruple-precision number:

    ┌─────────────────────┬─────────────┬──────────────┬───────────────────┐
    │ number format       │ field width │ stored value │ interpreted value │
    ├─────────────────────┼─────────────┼──────────────┼───────────────────┤
    │ single-precision    │ 8           │ 1..254       │ -126..127         │
    ├─────────────────────┼─────────────┼──────────────┼───────────────────┤
    │ double-precision    │ 11          │ 1..2046      │ -1022..1023       │
    ├─────────────────────┼─────────────┼──────────────┼───────────────────┤
    │ quadruple-precision │ 15          │ 1..32766     │ -16382..16383     │
    └─────────────────────┴─────────────┴──────────────┴───────────────────┘

### What are the two stored values which are processed specially?

The  values full  of 0s  and  full of  1s  (i.e. 0 and  255 in  single-precision
format).

####
## What's the single-precision format floating-point representation for
### 11/2?

    11/2 = (101.1)₂ = (1.011)₂ × 2^2

    ┌───┬──────────┬─────────────────────────┐
    │ 0 │ 10000001 │ 01100000000000000000000 │
    └───┴──────────┴─────────────────────────┘

Notice that:

   - the exponent is `2+127`
   - the fraction field doesn't contain the initial 1; it's hidden.

### 71?

    71 = (1000111)₂ = (1.000111)₂ × 2^6

    ┌───┬──────────┬─────────────────────────┐
    │ 0 │ 10000101 │ 00011100000000000000000 │
    └───┴──────────┴─────────────────────────┘

`10000101` is the stored exponent 133 (127 + 6).

### 1?

    1 = (1)₂ = (1.0)₂ × 2^0

    ┌───┬──────────┬─────────────────────────┐
    │ 0 │ 01111111 │ 00000000000000000000000 │
    └───┴──────────┴─────────────────────────┘

### 2^71?

    2^71 = (1.0) × 2^71

    ┌───┬──────────┬─────────────────────────┐
    │ 0 │ 11000110 │ 00000000000000000000000 │
    └───┴──────────┴─────────────────────────┘

##
## In single-precision format, what's the
### largest number?

                                       ┌ can't use the exponent 128, because it's interpreted specially
                                       │
      (1.11111111111111111111111)₂ × 2^127

    =  (2^-23 + 2^-22 + ... + 2^0) × 2^127

    =  2^(0+1) − 2^-23  × 2^127
       ───────────────
             2 − 1

    =  (2 − 2^-23) × 2^127

    =  2^128 − 2^104

    ≈ 3.4 × 10^38

###
### smallest positive
#### normalized number?

                                      ┌ can't use the exponent -127, because it's interpreted specially
                                      │
    (1.00000000000000000000000)₂ × 2^-126
    =
    2^-126
    ≈
    1.2 × 10^-38

#### subnormal number?

    (0.00000000000000000000001) × 2^-126
    =
    2^-149

#### **integer** that is not exactly representable?

There are two reasons which could explain why an integer is not exactly representable:

   - the exponent is too big (> 126)
   - the significand has too many bits (> 23)

Since we're  looking for the  smallest integer, and  the significand has  a much
lesser impact on the magnitude of a  number compared to the exponent, we need to
find the smaller integer whose significand contains 24 bits; that is:

    1.000000000000000000000000 × 2^24
    =
    2^24
    =
    16777216

---

You could think the answer is 2^23, because the latter needs 24 bits (a 1 then 24 0s).
But you  would be wrong,  because in a floating-point  number, the first  bit is
hidden; i.e. the computer assumes it's 1.
So, the computer would only need 23 bits to store the significand of 2^23, and not 24.

##
## A number which is not a floating-point number must be truncated.
### Why does the computer normalize it before, instead of after?

To get a more precise result.

Here's how 0.1 would be stored if its representation was truncated before being normalized:

    0.1 = (0.00011001100110011001100...)₂
        ≈ (0.00011001100110011001100)₂
        ≈ (1.10011001100110011000000)₂ × 2^4
                                ^--^
                                default 0s; not correct here

Here's how 0.1 is stored when its representation is normalized before being truncated:

    0.1 = (0.00011001100110011001100...)₂
        = (1.10011001100110011001100...)₂ × 2^4
        ≈ (1.10011001100110011001100)₂ × 2^4
                                ^--^
                                better; more accurate

###
## What's the floating-point representation of the number zero?

The number *zero* is special.
A pattern of only zeros in the  significand field represents 1.0, not 0.0, since
the bit  `b₀` is hidden and  its value is always  assumed to be 1,  so you can't
represent 0 without some trick.

The way  the IEEE standard  addresses this difficulty is  to use a  special zero
bitstring for the exponent  field, as well as a zero  bitstring for the fraction
field.

### How is interpreted a number whose exponent field contains only 0s, and significand field contains at least a 1?

As a subnormal.

##
## Why is it useful for a system to be able to represent ±∞?

It allows the  possibility of dividing a  number by zero and  storing a sensible
mathematical result, namely ±∞, instead of terminating with an overflow message.
Although one must be careful about what is meant by such a result.

### How is it stored?

All the bits  of the exponent field are  1, and all the bits  of the significand
field are 0.

### How is interpreted a number whose exponent field contains only 1s, and significand field contains at least a 1?

NaN: Not A Number.

##
## Assuming the precision of a system is 24, what's `ulp(x)` when `x` is:
### `0.25`

    ε = 2^(1 − 24) = 2^-23

    0.25 = (.01)₂ = (1.0)₂ × 2^-2
    ulp(0.25) = ε × 2^-2
              = 2^-25

### `2`

    2 = (10)₂ = (1.0)₂ × 2^1
    ulp(2) = ε × 2^1
           = 2^-22

### `3`

    3 = (11)₂ = (1.1)₂ × 2^1
    ulp(3) = ε × 2^1
           = 2^-22

### `4`

    4 = (100)₂ = (1.00)₂ × 2^2
    ulp(4) = ε × 2^2
           = 2^-21

### `10`

    10 = (1010)₂ = (1.010)₂ × 2^3
    ulp(10) = ε × 2^3
            = 2^-20

### `100`

    100 = (1100100)₂ = (1.100100)₂ × 2^6
    ulp(100) = ε × 2^6
             = 2^-17

### `1030`

    1030 = (10000000110)₂ = (1.0000000110)₂ × 2^10
    ulp(1030) = ε × 2^10
              = 2^-13

###
## How many floating-point numbers are there between two consecutive power of 2?

    2^(p − 1)

`p` being the precision of the floating-point system.

## What's the effect of increasing the size of the significand of a floating-point system by one bit?

It doubles the number of floating-point numbers between two consecutive power of
2, which makes the system more precise,  because the error between a real number
that you want to express in this system and its approximation reduces.
Hence the name “precision”.

---

For example, if  the precision of the  system is 3 (`1.b₁b₂`),  and the exponent
can vary between -1 and 2, the representable floating-point numbers would be:

    |───────|─|─|─|─|───|───|───|───|───────|───────|───────|───────|
    0               1               2               3               4

Here, there are 4 floating-point numbers  between 1 (included) and 2 (excluded),
and 4 floating-point numbers between 2 (included) and 4 (excluded).

Now,  if  you increase  the  precision  of the  system  to  4 (`1.b₁b₂b₃`),  the
representable floating-point numbers would become:

    |───────|||||||||─|─|─|─|─|─|─|─|───|───|───|───|───|───|───|───|
    0               1               2               3               4

This  time, there  are  8  floating-point numbers  between  1  (included) and  2
(excluded), and 8 floating-point numbers between 2 (included) and 4 (excluded).

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

Talk  about  the  biased  representation  as  opposed  to  the  sign-and-modulus
representation, and the 2's complement representation.

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

    x + (-y)

where

    0 ≤ x ≤ 2^31 − 1
    1 ≤ y ≤ 2^31

Clearly, it  is possible  to store the  desired result `x  − y`  without integer
overflow.
The result may be positive, negative, or  zero, depending on whether `x > y`, `x = y`,
or `x < y`.

---

Prove that when computing `x − y` via the 2's complement representations for `x`
and `-y`, the result is indeed `x − y`.


Case 1, `x ≥ y`:

`x − y` is computed like so:

      x + (2^32 − y)
    = 2^32 + (x − y)

Since `x ≥ y`, we know that `x − y` is a positive number.
So, the  leftmost bit  of the result  is an overflow  bit, corresponding  to the
power `2^32`, but this bit can be discarded, giving the correct result `x − y`.

If `x <  y`, the result fits  in 32 bits with  no overflow bit, and  we have the
desired  result, since  it  represents the  negative  value `−(y  −  x)` in  2's
complement.


Case 2, `x < y`:

`x − y` is computed like so:

      x + (2^32 − y)
    = 2^32 − (y − x)

Since `x < y`, we know that `y − x` is a positive number.
So, the  result fits in 32  bits with no overflow  bit, and we have  the desired
result, since it represents the negative value `−(y − x)` in 2's complement.


This demonstrates  an important  property of  2's complement  representation: no
special hardware is needed for integer subtraction.
The  addition hardware  can  be used  once  the negative  number  `-y` has  been
represented using 2's complement.

