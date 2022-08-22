# Purpose: use f-strings
# Reference: page 21 (paper) / 59 (ebook)

first_name = 'ada'
last_name = 'lovelace'
full_name = 'Ada Lovelace'

# An f-string lets you interpolate an arbitrary expression. {{{1

#           stands for "f"ormat (because Python formats the string when evaluating it)
#           v
full_name = f'{first_name} {last_name}'
#             ^          ^

# Anything inside the braces is evaluated  as an expression; the result replaces
# the braces and their contents in the evaluation of the embedding f-string.
print(full_name)
#     ada lovelace

# In an f-string, expressions can be mixed with literal texts. {{{1

#       literal text     method call
#       v-----v          v------v
print(f'Hello, {full_name.title()}!')
#     Hello, Ada Lovelace!
#
# You're not limited to simple variables; all expressions are valid.

# f-strings are allowed anywhere a regular string is allowed. {{{1

# That includes the LHS of an assignment:
message = f'Hello, again, {full_name.title()}!'
print(message)
#     Hello, again, Ada Lovelace!

# f­strings require 3.6 or later. {{{1

# If you're using Python  3.5 or earlier, you need to  use the `format()` method
# instead:
full_name = '{}, {}'.format(first_name, last_name)
#            ^^  ^^ ^------^
#
# All  the pair  of braces  will be  replaced with  the expressions  provided as
# arguments to `format()`; in the order they've been passed.  This is similar to
# how format specifiers (e.g. `%s` and `%d`) work with `printf(1)`.

print(full_name)
#     ada, lovelace
