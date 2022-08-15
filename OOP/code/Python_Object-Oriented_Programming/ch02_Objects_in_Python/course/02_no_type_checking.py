# Purpose: code without type checking
# Reference: page 40 (paper) / 61 (ebook)


def odd(n):
    return n % 2 != 0

print(odd(3))
#     True
print(odd(4))
#     False

# So far, so good.  Now, let's see what happens if we pass an expression with an
# invalid type:
print(odd('Hello, world!'))
#     TypeError: not all arguments converted during string formatting
#
# Python did not complain about the type  of the `n` paramater being wrong (e.g.
# "expected number  but got  string").  It  happily passed  our wrong  string to
# `odd()`.  But in the end, an exception is still raised when computing `n % 2`.
# Since `n` is a string, `%` is parsed as an interpolation operator, like here:
#
#     print('aaa %d bbb' % 123)
#     aaa 123 bbb˜
#
# But our  string does  not contain  any format specifier  like `%d`,  so Python
# complains because it can't do anything with this `2` argument:
#
#     return n % 2 != 0
#                ^
#                ✘
