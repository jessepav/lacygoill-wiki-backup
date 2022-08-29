# Purpose: do some arithmetic on non-integer numbers
# Reference: page 79

import sys
from fractions import Fraction as F
from decimal import Decimal as D
import decimal

# Real numbers {{{1
# Creation {{{2

pi = 3.1415926536
radius = 4.5
# A = π * r²
area = pi * (radius ** 2)
print(area)
#     63.617251235400005

# Approximation {{{2

# There is  an infinite number  of real numbers, but  Python works on  a machine
# with limited amount  of resources (memory/CPU/time/...).  As a  result, only a
# subset of real numbers can be  represented.  Let's see how Python handles them
# internally on the current system:
print(sys.float_info)
#     sys.float_info(
#     max=1.7976931348623157e+308,
#     max_exp=1024,
#     max_10_exp=308,
#     min=2.2250738585072014e-308,
#     min_exp=-1021,
#     min_10_exp=-307,
#     dig=15,
#     mant_dig=53,
#     epsilon=2.220446049250313e-16,
#     radix=2,
#     rounds=1)

# Since only *some*  real numbers can be represented, a  real number often needs
# to be approximated.  This is an issue which is not limited to very big or very
# small numbers:
print(0.3 - 0.1 * 3)
#     -5.551115123125783e-17
#
# The previous result should be 0, but it's not.
# That's because even a number such as `0.1` needs to be approximated.
# Indeed, numbers  are stored  in binary,  and in binary  `0.1` has  an infinite
# number of digits after the binary point:
#
#     1/10 = (0.0001100110011...)₂ = 1/16 + 1/32 + 0/64 + 0/128 + 1/256 + 1/512 + 0/1024 + ...
#              ^
#              binary point
#
# Obviously,  Python  can't save  an  infinite  number  of  digits, so  in  some
# computations, it  might have  to approximate  a real  number, which  gives the
# previous unexpected result.
# }}}1
# Complex numbers {{{1
# Creation {{{2

# In math, the imaginary unit is noted `i`, but engineers use `j` instead.
# Python uses `j` too:
#
#              v
c = 3.14 + 2.73j
print(c)
print(type(c))
#     (3.14+2.73j)
#     <class 'complex'>
#             ^-----^

# A complex number can also be expressed with the `complex()` function:
c = complex(3.14, 2.73)
print(c)
#     (3.14+2.73j)

# Real and imaginary parts {{{2

# The  `real` and  `imag`  attributes of  a  complex number  give  its real  and
# imaginary parts:
print(c.real)
print(c.imag)
#     3.14
#     2.73

# Conjugate {{{2

# The `conjugate()` method gives the conjugate of a complex number:
print(c.conjugate())
#     (3.14-2.73j)

# Arithmetic {{{2

# Complex numbers support usual arithmetic operations such as multiplication and
# exponentiation:
print(c * 2)
print(c ** 2)
#     (6.28+5.46j)
#     (2.4067000000000007+17.1444j)

# As well as addition and subtraction:
d = 1 + 1j
print(c + d)
print(c - d)
#     (4.140000000000001+3.73j)
#     (2.14+1.73j)
# }}}1
# Fractions {{{1
# Creation {{{2

# For computations  involving rational  numbers, the `Fraction()`  function from
# the `fractions` module gives more accurate results than with floats:
print(F(10, 6))
#     5/3

print(F(1, 3) + F(2, 3))
#     1

# `Fraction()` expects integers or fractions:
#
#          ✔     ✔
#       v-----v  v
print(F(F(6, 5), 3))
#     2/5

# But not floats  (even if they can be  expressed as a fraction; a  float is not
# internally stored like a Rational):
#
#        ✘
#       vvv
print(F(1.2, 3))
#     TypeError: both arguments should be Rational instances

# Numerator / denominator {{{2

# The `numerator` and `denominator`  attributes of a `fractions.Fraction` object
# give its numerator and denominator:
f = F(10, 6)
print(f.numerator)
print(f.denominator)
#     5
#     3
# }}}1
# Decimal numbers {{{1
# Creation {{{2

# If you're working  with decimal numbers instead of fractions,  you can use the
# `Decimal()` function from  the `decimal` module.  But it costs  more space and
# more CPU time.

# Don't  pass   a  number  to  `Decimal()`.    The  latter  would  work   on  an
# approximation, which is not what you want:
#
#        ✘
#       v--v
print(D(3.14))
#     3.140000000000000124344978758017532527446746826171875

# Instead, pass a string representation of your decimal number:
#
#       ✔    ✔
#       v    v
print(D('3.14'))
#     3.14

# No need  to use `Decimal()`  for integers (because in  that case, there  is no
# approximation):
#
#                v
#
print(D('0.1') * 3 - D('0.3'))
#     0.0

# As fractions {{{2

# The  `as_integer_ratio()`  method  of  a `decimal.Decimal`  object  gives  the
# numerator and  denominator of the irreducible  fraction which is equal  to the
# decimal number:
print(D('1.4').as_integer_ratio())
#     (7, 5)

# Precision {{{2

# The `getcontext()` and `setcontext()` methods change the precision of decimal numbers:
#
#           v----------v
c = decimal.getcontext()
old = c.prec
c.prec = 12
decimal.setcontext(c)
#       ^-----------^
new = c.prec
print(old, new)
#     28 12
