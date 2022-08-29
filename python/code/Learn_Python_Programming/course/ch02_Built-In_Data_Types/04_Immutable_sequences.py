# Purpose: work with immutable sequences
# Reference: page 83

from math import pi

small_primes = frozenset([2, 3, 5, 7])
bigger_primes = frozenset([5, 7, 11])

# There are 4 types of immutable sequences:{{{
#
#    - strings
#    - bytes objects
#    - tuples
#    - frozen sets
#}}}

# Strings {{{1
# Sometimes, a printed string might end with a trailing whitespace:{{{
#
#     >>> print('abc ')
#     abc▫
#        ^
#        trailing whitespace
#
# which is brittle  (we might use a command which  removes it automatically) and
# ugly (we might have some config which highlights it).
#
# To avoid this, use the `repr()` function:
#
#               v--v
#     >>> print(repr('abc '))
#     'abc '
#     ^    ^
#
# The  latter  will print  the  canonical  representation  of the  string  which
# includes quotes; this way no more trailing whitespace.
#}}}
# Creation {{{2

str1 = 'This is a string.  We built it with single quotes.'
str2 = "This is also a string, but built it with double quotes."
str3 = '''This is built using triple quotes,
so it can span multiple lines.'''
str4 = """This too
is a multiline one built with triple double-quotes."""

print(str1)
#     This is a string.  We built it with single quotes.
print(str2)
#     This is also a string, but built it with double quotes.
print(str3)
#     This is built using triple quotes,
#     so it can span multiple lines.
print(str4)
#     This too
#     is a multiline one built with triple double-quotes.

# Length {{{2

# The `len()` function gives the length of a string.
str1 = 'This is a string.  We built it with single quotes.'
print(len(str1))
#     50

# Prefix / suffix {{{2

# The `removeprefix()` and `removesuffix()` methods remove the prefix or suffix of a string.
s = 'Hello There'
print(s.removeprefix('Hell'))
print(s.removesuffix('here'))
print(s.removeprefix('Ooops'))
#     o There
#     Hello T
#     Hello There

# Indexing / slicing {{{2

s = 'The trouble is you think you have time.'

# The `[n]` syntax indexes a string at position `n`:
print(s[0])
print(s[5])
#     T
#     r

# The `[start:stop]` syntax slices a string.{{{
#
# `start` must  be the index  of the first  character in the  desired substring,
# while `end` must  be the index of  the character *after* the  last one (that's
# because `end` is exclusive contrary to `start`).
#}}}
# Here, we omit `start`, which defaults to 0.{{{
#
# Actually, `start` defaults to 0 when `step` is positive (more on `step` later).
# If `step` is negative, `start` defaults to `-1`.
#}}}
print(repr(s[:4]))
#     'The '

# In a slice, all indexes can be omitted.
# If you omit the last one, the substring goes to the end.
# BTW,  it's the  only way  to  include the  last character;  because `stop`  is
# exclusive:
print(s[4:])
#     trouble is you think you have time.

# Both indexes can be explicit:
print(s[2:14])
#     e trouble is

# The syntax for a slice accepts a third optional index: `step`.
# The latter expresses by how much  the index should be incremented when looking
# for the next character in the slice (it defaults to 1):
print(repr(s[2:14:3]))
#     'erb '

# `[:]` is a special syntax which lets you get a copy of a string:
print(s[:])
#     The trouble is you think you have time.

# `[::-1]` is another special syntax which lets you reverse a string:
s = 'edcba'
print(s[::-1])
#     abcde

# Formatt] 
# Formatting {{{2

# The `format()` method formats strings.

# It  operates  on a  format  string  which must  include  one  or several  `{}`
# placeholders, and it  expects as many arguments as placeholders.   Each of its
# arguments replaces the  placeholder which has the same position  in the format
# string:
#
#                         vv
greet_positional = 'Hello {}!'
print(greet_positional.format('Fabrizio'))
#     Hello Fabrizio!

#                         vv vv
greet_positional = 'Hello {} {}!'
print(greet_positional.format('Fabrizio', 'Romano'))
#     Hello Fabrizio Romano!

# The placeholders  can contain indexes.   In that  case, each of  its arguments
# replaces the placeholder which has the same index:
#
#                                v     v         v
greet_positional_idx = 'This is {0}!  {1} loves {0}!'
print(greet_positional_idx.format('Python', 'Heinrich'))
print(greet_positional_idx.format('Coffee', 'Fab'))
#     This is Python!  Heinrich loves Python!
#     This is Coffee!  Fab loves Coffee!

# Finally,  the placeholders  can contain  arbitrary keywords.   In which  case,
# `format()` expects keyword arguments (`kwd=value`), and each of those replaces
# the placeholder(s) sharing the same keyword:
#
#                             v--v   v-------v
keyword = 'Hello, my name is {name} {last_name}'
print(keyword.format(name='Fabrizio', last_name='Romano'))
#                    ^--^             ^-------^
#
#     Hello, my name is Fabrizio Romano

# f-strings {{{2

# Formatted string literals (aka f-strings) include formatting natively.

# This is easier to read/use and faster than `format()`, but requires Python 3.8.

# f-strings also include curly braces, but they serve a different purpose.
# They are no longer placeholders, but replacement fields.
# Each of them is meant to include  an expression which is evaluated at runtime;
# the result then replaces the braces and everything they contain:
name = 'Fab'
age = 42
print(f"Hello!  My name is {name} and I'm {age}")
#     Hello!  My name is Fab and I'm 42

print(f"No arguing with {pi}, it's irrational...")
#     No arguing with 3.141592653589793, it's irrational...

# Optionally, an expression  inside a replacement field can be  appended with an
# equal sign  specifier.  If such a  sign is present, inside  the output string,
# the evaluation  is prefixed with  the original  expression and an  equal sign.
# This is useful for debugging and self-documenting:
user = 'heinrich'
password = 'super-secret'
print(f'Log in with: {user} and {password}')
#                         v               v
print(f'Log in with: {user=} and {password=}')
#     Log in with: heinrich and super-secret
#     Log in with: user='heinrich' and password='super-secret'
#                  ^---^               ^-------^
#
# This syntax requires Python 3.8.
# }}}1
# Bytes objects {{{1

# The `b` prefix in front of a string specifies a bytes object:
#
#           v
bytes_obj = b'A bytes object'
print(type(bytes_obj))
#     <class 'bytes'>

# The `encode()` method encodes a string into a bytes object:
s = 'This is üŋíc0de'
encoded_s = s.encode('utf-8')
print(encoded_s)
#     b'This is \xc3\xbc\xc5\x8b\xc3\xadc0de'
#               ^^
# The `\x..` escape sequences match the actual bytes encoding the characters.{{{
#
# For example,  in Vim, if  you press  `g8` on `ü`,  `ŋ`, and `í`,  these hex
# codes are printed:
#
#     c3 bc
#     c5 8b
#     c3 ad
#
# They match these escape sequences in the previous Python bytes object:
#
#     b'This is \xc3\xbc\xc5\x8b\xc3\xadc0de'
#               ^------^^------^^------^
#}}}

# The result is a bytes object:
print(type(encoded_s))
#     <class 'bytes'>

# The `decode()` method decodes a bytes object into a UTF-8 string:
print(encoded_s.decode('utf-8'))
#     This is üŋíc0de
# }}}1
# Tuples {{{1
# Creation {{{2

# An empty tuple is expressed as `()`:
t = ()
print(type(t))
#     <class 'tuple'>
#             ^---^

# A tuple with only 1 item is expressed as `(item,)`.
# The comma is mandatory.{{{
#
# Without the parens are ambiguous.
# Are they meant to express a tuple?
# Or are they meant to group operations inside an expression?
# Without a comma, Python assumes the latter.
#}}}
#                      v
one_element_tuple = (42,)
# The general syntax is `(item, ...)`.
three_elements_tuple = (1, 3, 5)

# Multi-assignment {{{2

# Tuples can be used to execute multiple assignments in a single statement:
(a, b, c) = (1, 2, 3)
# In that case, the parens can be omitted:
a, b, c = 1, 2, 3
# Parens can also be omitted when assigning a tuple to a single variable:
my_tuple = 1, 2, 3
# They can even be omitted when printing a tuple in a REPL:{{{
#
#     >>> a, b, c
#     (1, 2, 3)
#
# It also works with `print()`:
#
#     print(a, b, c)
#
# But  I think  that's only  because  `print()` accepts  several arguments;  not
# because it accepts a tuple.
#}}}

# Swap {{{2

# An assignment with implicit tuples is handy to swap values between variables:
a, b = 1, 2
a, b = b, a
print(a, b)
#     2 1

# Membership test {{{2

# A tuple supports the membership operator `in`:
#
#       vv
print(3 in three_elements_tuple)
#     True
#
# So do lists, strings, dictionaries, and more generally sequence objects.
# }}}1
# Frozen sets {{{1
# They are similar to regular sets, except they can't mutate.
# Disallowed methods {{{2

# The `add()` method can't add a value to a frozen set:
small_primes.add(11)
#     AttributeError: 'frozenset' object has no attribute 'add'

# The `remove()` method can't remove a value from a frozen set:
small_primes.remove(2)
#     AttributeError: 'frozenset' object has no attribute 'remove'

# Allowed operators {{{2

# The `|`, `&`, `-` accept frozen sets as operands (because they don't make them mutate):
print(small_primes | bigger_primes)
print(small_primes & bigger_primes)
print(small_primes - bigger_primes)
#     frozenset({2, 3, 5, 7, 11})
#     frozenset({5, 7})
#     frozenset({2, 3})
