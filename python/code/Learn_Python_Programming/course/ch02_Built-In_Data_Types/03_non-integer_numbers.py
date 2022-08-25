# Purpose: do some arithmetic on non-integer numbers
# Reference: page 79

import sys
from fractions import Fraction as F
from decimal import Decimal as D
import decimal

# real numbers {{{1

pi = 3.1415926536
radius = 4.5
# A = π * r²
area = pi * (radius ** 2)
print(area)
#     63.617251235400005

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

# complex numbers {{{1

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

# a complex number can also be expressed with the `complex()` function
c = complex(3.14, 2.73)
print(c)
#     (3.14+2.73j)

# you can retrieve the real and imaginary parts of a complex number object using
# its `real` and `imag` attributes
print(c.real)
print(c.imag)
#     3.14
#     2.73

# you can get the conjugate of a complex number via the `conjugate()` method
print(c.conjugate())
#     (3.14-2.73j)

# complex numbers support usual arithmetic operations such as multiplication and
# exponentiation
print(c * 2)
print(c ** 2)
#     (6.28+5.46j)
#     (2.4067000000000007+17.1444j)

# as well as addition and subtraction
d = 1 + 1j
print(c + d)
print(c - d)
#     (4.140000000000001+3.73j)
#     (2.14+1.73j)

# fractions {{{1

# You can get more accurate results  than with floats for computations involving
# rational numbers, using the `Fraction()` function from the `fractions` module:
print(F(10, 6))
#     5/3

print(F(1, 3) + F(2, 3))
#     1

# You  can also  access the  numerator  and denominators  separately, using  the
# `numerator` and `denominator` attributes of the `fractions.Fraction` object:
f = F(10, 6)
print(f.numerator)
print(f.denominator)
#     5
#     3

# `Fraction()` expects integers or fractions:
#
#          ✔     ✔
#       v-----v  v
print(F(F(6, 5), 3))
#     2/5

# But not floats (even  if they can be expressed as a fraction;  a float is notj
# internally stored like a Rational):
#
#        ✘
#       vvv
print(F(1.2, 3))
#     TypeError: both arguments should be Rational instances

# decimal numbers {{{1

# If you're working  with decimal numbers instead of fractions,  you can use the
# `Decimal()` function from  the `decimal` module.  But it costs  more space and
# more CPU time.

# Don't  pass   a  number  to  `Decimal()`.    The  latter  would  work   on  an
# approximation, which is not what you want.
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

# You can get the numerator and denominator of the irreducible fraction which is
# equal to your decimal number, invoking the `as_integer_ratio()` method on your
# `decimal.Decimal` object:
#
#              v----------------v
print(D('1.4').as_integer_ratio())
#     (7, 5)

# You can change  the precision of decimal numbers using  the `getcontext()` and
# `setcontext()` methods:
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
