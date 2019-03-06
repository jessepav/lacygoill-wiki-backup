# b
## bit

Abbreviation for binary digit.

You can view it as a single physical entity in one of two states: on or off.

## bitstring

A string of bits.

##
# e
## expansion (of a number)

A sum of powers of the base, each  power being multiplied by one of the digit of
the number:

    (71)₁₀ = 7 × 10 + 1
             ├────────┘
             └ expansion of 71 in base 10

    (1000111)₂ = 1 × 64 + 0 × 32 + 0 × 16 + 0 × 8 + 1 × 4 + 1 × 2 + 1 × 1
                 ├──────────────────────────────────────────────────────┘
                 └ expansion of 71 in base 2

Also used as a synonym for “representation (of a number)”.

##
# f
## floating-point (representation)

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
## (computer number) format

The internal representation of numeric values in digital computer.

The encoding between numerical values and bit patterns is chosen for convenience
of the operation of the computer.
Different types  of processors  may have  different internal  representations of
numerical values.

## fractional part (of the significand), fraction field

The bits following the binary point in the representation of a floating-point number.

##
# h
## hidden bit

First bit of the significand of a floating-point number?

No matter the number, it's always 1.

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

