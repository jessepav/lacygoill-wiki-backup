# Purpose: use numbers
# Reference: page 25 (paper) / 63 (ebook)

# Python supports the usual mathematical arithmetic operators. {{{1

print(2 + 3)
#     5

print(3 - 2)
#     1

print(2 * 3)
#     6

print(3 / 2)
#     1.5

print(4 / 2)
#     2.0
#
# Notice  how  the result  of  a  division is  always  a  float; even  when  the
# mathematical result is an integer.

# The exponentiation operator is written `**` (not `^`). {{{1

# 3²
print(3 ** 2)
#     9

# 3³
print(3 ** 3)
#     27

# 10⁶
print(10 ** 6)
#     1000000

# Each operator has a precedence level, and an associativity (left, right). {{{1
# They determine how operations are grouped.

print(2 + 3 * 4)
#     14
#
# Here, the operations are implicitly grouped like this:
#
#     print((2 + (3 * 4)))
#     #     ^-----------^
#
# Because `*` has a higher precedence than `+`.
# So, the operands around `*` are grouped first.

# And like in math, you can change the grouping using parentheses:
#     v     v
print((2 + 3) * 4)
#     20
#
# Notice that the  result is different even though the  expression is mostly the
# same.   That's because  the parentheses  have  changed the  precedence of  `+`
# making it higher than `*`.

# Python supports floats in arithmetic computations. {{{1

print(0.1 + 0.1)
#     0.2
print(0.2 + 0.2)
#     0.4
print(2 * 0.1)
#     0.2
print(2 * 0.2)
#     0.4

# but the result might sometimes be unexpected:
print(0.2 + 0.1)
#     0.30000000000000004
#        ^--------------^
#
# Here, you probably didn't expect these 16 trailing digits.
# But that's an artefact of how floats are represented internally by the CPU.{{{
#
# Some floats cannot be represented exactly  in binary.  For example, in binary,
# the representation of `0.1` is infinite:
#
#     1/10 = (0.0001100110011...)₂ = 1/16 + 1/32 + 0/64 + 0/128 + 1/256 + 1/512 + 0/1024 + ...
#
# Obviously,  the CPU  can't  save an  infinite  number of  digits,  so in  some
# computations, it might  have to approximate a float, which  gives the previous
# unexpected result.
#
# BTW, all programming languages have to deal with this issue.
# Example in Ruby:
#
#     $ irb
#     > 0.1 + 0.2
#     => 0.30000000000000004
#           ^--------------^
#}}}

# It is allowed to mix a float and an integer in an arithmetic computation. {{{1
# The result is then always a float.

print(1 + 2.0)
#     3.0
print(2 * 3.0)
#     6.0
print(3.0 ** 2)
#     9.0

# It is allowed to include underscores in a long number to make it more readable. {{{1

universe_age = 14_000_000_000
print(universe_age)
#     14000000000

# It is possible to assign values to several variables in a single statement. {{{1
# By separating 2 consecutive variables/values with  a comma, and by writing the
# same amount of variables/values.

#v  v      v  v
x, y, z = 1, 2, 3
print(x, y, z)
#     1 2 3

# Python does not support a constant type, but there exists a widely adopted convention. {{{1
# It states  that the  value of  a variable whose  name only  contains uppercase
# letters is never meant to change (which makes it a constant).

MAX_CONNECTIONS = 5000
