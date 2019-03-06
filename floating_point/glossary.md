# a
## arithmetic

Branch of  mathematics that  consists of  the study  of numbers,  especially the
properties  of  the traditional  operations  on  them —  addition,  subtraction,
multiplication and division.

##
# b
## bit

Abbreviation for binary digit.

You can view it as a single physical entity in one of two states: on or off.

## bitstring

A string of bits.

##
# e
## expansion (of a number)

A sum of powers of the base of the number, each power being multiplied by one of
the digit of the number:

    (71)₁₀ = 7 × 10 + 1
             ├────────┘
             └ expansion of 71 in base 10

    (1000111)₂ = 1 × 64 + 0 × 32 + 0 × 16 + 0 × 8 + 1 × 4 + 1 × 2 + 1 × 1
                 ├──────────────────────────────────────────────────────┘
                 └ expansion of 71 in base 2

Also used as a synonym for “representation (of a number)”.

##
## exponent bias

An integer  number added  to the  exponent of a  floating-point number  when the
latter must be stored in memory.

<https://en.wikipedia.org/wiki/Exponent_bias>

### Why is it necessary?

Exponents are signed values, but two's complement – the usual representation for
signed values – would make comparison harder.

### How is it computed?

    2^(k-1) — 1

`k` is the size in bits of  the exponent field; that is 8 (single-precision), 11
(double-precision) or 15 (quadruple-precision).

Thus, its value is one of:

    2^(8-1) — 1  = 127
    2^(11-1) — 1 = 2047
    2^(15-1) — 1 = 32767

### How is it used?

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

#
# f
## floating-point representation

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
## floating-point system

A floating-point system is characterized by four integers:

   - a radix `β ≥ 2`

   - a precision `p ≥ 2`

     Roughly  speaking,  `p`  is  the  number of  “significant  digits”  of  the
     representation.

   - two extremal exponents `eₘᵢₙ` and `eₘₐₓ` such that `eₘᵢₙ < eₘₐₓ`

     In all practical cases,  `eₘᵢₙ < 0 < eₘₐₓ`, and  with all formats specified
     by the IEEE 754 standard, `eₘᵢₙ = 1 − eₘₐₓ`.

It allows the representation of finite floating-point numbers `x`, such that:

    x = S × β^e

where:

   - `S` is a real number such that `1 ≤ |S| < β`, called the significand of the
     representation of `x`

   - `e` is an integer such that `eₘᵢₙ ≤ e ≤ eₘₐₓ`, called the exponent of the
     representation of `x`

##
## (computer number) format

The internal representation of numeric values in digital computer.

The encoding between  numerical values and bitstrings is  chosen for convenience
of the operation of the computer.
Different types  of processors  may have  different internal  representations of
numerical values.

## fractional part (of the significand), fraction field

The bits following the binary point in the representation of a floating-point number.

##
# h
## hidden bit

First bit of the significand of a floating-point number.

The first bit of a floating-point number is always 1.

### Why is it called like this?

Because it's not stored since it doesn't need to be.

###
# i
## IEEE

Institute for Electrical and Electronics Engineers.

Pronounced “I triple E.”

## integer overflow

Integer overflow occurs when two positive  or negative integers of the same sign
are added together, and the result gives an integer `≥ 2^31` or `< -2^31`.

If the integers have different signs, no integer overflow can occur:

    (1):     0 ≤ x ≤ 2^31 — 1
    (2): —2^31 ≤ y ≤ 0

    (1) ∧ (2) ⇒     —2^31 ≤ x + y ≤ 2^31 — 1

##
# n
## non-terminating

Qualify the representation of a real number which is not finite.

## numeral system

Writing  system for  expressing numbers;  that is,  a mathematical  notation for
representing  numbers  of a  given  set,  using digits  or  other  symbols in  a
consistent manner.

The  same sequence  of  symbols  may represent  different  numbers in  different
numeral systems.
For example,  "11" represents the number  eleven in the decimal  numeral system,
and the number three in the binary numeral system.

The number the numeral represents is called its value.

Numeral systems are sometimes called number systems, but that name is ambiguous,
as it could  refer to different systems  of numbers, such as the  system of real
numbers, the system of complex numbers, etc.

<https://en.wikipedia.org/wiki/Numeral_system>

##
# o
## overflow bit

Excessive bit  produced when the  size of the result  of an operation  is bigger
than the operands.

For example, if you  sum two 32-bit words, and the result  contains 33 bits, you
have an overflow bit.

### How is such a bit processed?

It's discarded.

##
# p
## (decimal, binary, radix) point

Separation between the integer part and the fractional part of the
representation of a number.

    ┌───────────────┬────────────────────────────────┐
    │               │ applies to a representation in │
    ├───────────────┼────────────────────────────────┤
    │ decimal point │ decimal                        │
    ├───────────────┼────────────────────────────────┤
    │ binary point  │ binary                         │
    ├───────────────┼────────────────────────────────┤
    │ radix point   │ arbitrary base                 │
    └───────────────┴────────────────────────────────┘

## precision (of a floating-point format)

Number  of   bits  in  the  significand   field  of  the  representation   of  a
floating-point number, including the hidden bit.

##
# r
## repeating

Qualify  the   representation  of  a   real  number  whose  symbols   after  the
decimal/binary point repeat periodically.

## representation (of a number)

The sequence of symbols which expresses this number in a given base.

For example, the representation of seventy one  is `71` in base 10, and `1000111`
in base 2.

##
# s
## scientific notation (of a number `x`)

    ± S × 10^E

`S` is called the significand, and `E` the exponent.

### What's its normalized form?

    ± S × 10^E
    1 ≤ S < 10

##
# w
## word

4 consecutive bytes of computer storage (i.e. 32 bits).

## double word

8 consecutive bytes (64 bits).

