# Purpose: call methods on strings
# Reference: page 20 (paper) / 58 (ebook)

name = 'ada lovelace'

# The `title()` method. {{{1

#         v------v
print(name.title())
#     Ada Lovelace
#     ^   ^
#
# Notice how the `title()` method has capitalized each word in the string stored
# in `name`.

# We say that `title()` "title case" a string.
# The case of the input string does not matter; the output is always the same:
a = 'Ada'
b = 'ADA'
c = 'ada'
print(a.title())
print(b.title())
print(c.title())
#     Ada
#     Ada
#     Ada

# The `lower()` and `upper()` methods. {{{1

# Similarly, the `lower()` and `upper()` methods  can turn all characters from a
# string in lowercase or uppercase.
#
#         v------v
print(name.lower())
#         v------v
print(name.upper())
#     ada lovelace
#     ADA LOVELACE

# The `strip()`, `lstrip()` and `rstrip()` methods. {{{1

# To remove leading or trailing whitespace, you can use resp. the `lstrip()` and
# `rstrip()` methods.
favorite_language = ' python '
print(f'|{favorite_language}|')
#     | python |
#      ^      ^

#                                     v------v
favorite_language = favorite_language.lstrip()
print(f'|{favorite_language}|')
#     |python |
#            ^

#                                     v------v
favorite_language = favorite_language.rstrip()
print(f'|{favorite_language}|')
#     |python|

# To remove both with a single method call, use `strip()`.
#                              v-----v
favorite_language = ' python '.strip()
print(f'|{favorite_language}|')
#     |python|

# None of the methods seen so far operate in-place. {{{1

# That is, simply calling them on  a variable, without assigning the result back
# to the latter, does not change its value.
favorite_language = ' python '
favorite_language.strip()
print(f'|{favorite_language}|')
#     | python |
#      ^      ^
#
# Notice that the spaces  have not been stripped from the  value assigned to the
# `favorite_language` variable, even though `strip()` was called before.
# That's because `strip()` does not operate  in-place, and we did not assign the
# result of the method call back to the variable.
