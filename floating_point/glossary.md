# Where does the word “bit” come from?

It's an abbreviation for binary digit.

## How can I view it physically?

As a single physical entity in one of two states: on or off.

#
# How do you call a string of bits?

A bitstring.

# What can a byte represent?

Up to 256 bitstrings, which may be viewed as representing the integers from 0 to
255, or some characters.

The ASCII  encoding scheme  defines standard  character interpretations  for the
first 128 of these bitstrings.

#
# What is a “word”?

4 consecutive bytes of computer storage (i.e. 32 bits).

# What is a “double word”?

8 consecutive bytes (64 bits).

##
# What's the representation of a number?

The sequence of symbols which expresses this number in a given base.

For example, the representation of seventy one  is `71` in base 10, and `1000111`
in base 2.

# What's the expansion of a number?

A sum of powers of the base, each  power being multiplied by one of the digit of
the number:

    (71)₁₀ = 7 × 10 + 1
             ├────────┘
             └ expansion of 71 in base 10

    (1000111)₂ = 1 × 64 + 0 × 32 + 0 × 16 + 0 × 8 + 1 × 4 + 1 × 2 + 1 × 1
                 ├──────────────────────────────────────────────────────┘
                 └ expansion of 71 in base 2

# What's the difference between a decimal point, a binary point, and a radix point?

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

##
# How do you qualify the representation of a nonintegral real number
## which is not finite?

It's said to be “nonterminating”.

## whose symbols after the decimal/binary point repeat periodically?

It's said to be “repeating”.

##
# Give an example of number whose representation is finite in decimal, but not in binary.

0.1

In decimal, there's only one digit after the decimal point.
In binary, there's an infinite number of bits after the binary point:

    1/10 = (0.0001100110011...)₂ = 1/16 + 1/32 + 0/64 + 0/128 + 1/256 + 1/512 + 0/1024 + ...
            ├────────────────┘
            └ mnemonic: 0.0 then 0011, 0011, ...

##
# Which property is shared by
## all rational numbers?

Their representation is always either finite or repeating.

    1/7 = (0.142857142857)₁₀
             ├────┘├────┘
             │     └ period 2
             └ period 1

## all irrational numbers?

Their representation is neither finite nor repeating.

    √2 = (1.414213...)₁₀
    π  = (3.141592...)₁₀
    e  = (2.71828182845...)₁₀

#
# What's “integer overflow”?

Integer overflow occurs when two positive  or negative integers of the same sign
are added together, and the result gives an integer `≥ 2^31` or `< -2^31`.

If the integers have different signs, no integer overflow can occur:

    (1):     0 ≤ x ≤ 2^31 — 1
    (2): —2^31 ≤ y ≤ 0

    (1) ∧ (2) ⇒     —2^31 ≤ x + y ≤ 2^31 — 1

# If the result of an operation involving 32-bit words contains more than 32 bits, how are the excessive bits called?

Overflow bits.

## What happens to them?

They're discarded.

#
# What's the meaning of the acronym IEEE?

Institute for Electrical and Electronics Engineers.

## How is it pronounced?

“I triple E.”

