# Purpose: do some arithmetic on integers
# Reference: page 74

a = 14
b = 3

# Addition / subtraction / multiplication / division {{{1

print(a + b)
print(a - b)
print(a * b)
#     17
#     11
#     42

print(a / b)   # algebraic quotient
print(a // b)  # integer quotient
#     4.666666666666667
#     4

# Power {{{1

# `pow()` is an alternative function to the `**` operator:
print(10 ** 3)
print(pow(10, 3))
print(10 ** -3)
print(pow(10, -3))
#     1000
#     1000
#     0.001
#     0.001

# Exponentiation / modulo {{{1

print(a % b)   # modulo operation (remainder of division)
print(a ** b)  # exponentiation
#     2
#     2744

# Modular exponentiation {{{1

# `pow()`  accepts a  third optional  modulus  argument to  compute a  *modular*
# exponentiation:
print(pow(123, 4, 100))
#                 ^^^
#     41

# `pow()` supports  a negative  exponent.  It can  be set to  -1 to  compute the
# modular multiplicative inverse:
print(pow(37, -1, 43))
#             ^^
#     7
#
# Proof that the result is correct:
#      v
print((7 * 37) % 43)
#     1
#     ^

# Rounding {{{1

# `//` rounds down:
print(-7 // 4)
#     -2

# `int()` discards the fractional part:
print(int(-7 / 4))
#     -1

# Conversion {{{1

# `int()` can  convert the  string representation  of a  number expressed  in an
# arbitrary base into a decimal number:
print(int('10110', base=2))
#     22
#
# Here, `int()` converts the binary number 10110 into the decimal number 22.

# Readability {{{1

# A big number can include underscores to be more readable:
#      v   v   v
print(1_000_000_000)
#     1000000000
