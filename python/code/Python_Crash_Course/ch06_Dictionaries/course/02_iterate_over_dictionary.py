# Purpose: iterate over keys and values in dictionary
# Reference: page 99 (paper) / 137 (ebook)

favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python',
}

# A `for` loop can be used to iterate over the keys and values of a given dictionary. {{{1

user_0 = {
    'username': 'efermi',
    'first': 'enrico',
    'last': 'fermi',
}

#   vvv  v---v          v------v
for key, value in user_0.items():
    print(f'Key: {key}')
    print(f'Value: {value}\n')
#     Key: username
#     Value: efermi
#
#     Key: first
#     Value: enrico
#
#     Key: last
#     Value: fermi
#
# So far, `for` loops have always iterated over 1 variable.
# Here, we can see that `for` can let us iterate over more variables (2).
#
# That's only possible when the items of the list we iterate over are themselves
# nested lists or tuples. The `items()` method gives us a list of tuples:
print(user_0.items())
#     dict_items([('username', 'efermi'), ('first', 'enrico'), ('last', 'fermi')])
#                ^--------------------------------------------------------------^
#
# Each nested list/tuple must contain the same  number of items as the number of
# iteration variables.  On  a dictionary, the `items()` method  will always give
# us a list  of tuples each containing 2  items (a key and a  value).  Thus, the
# number of iteration variables must also be 2.

#   `key` and `value` can be named however you like. {{{1

#   v--v  v------v
for name, language in favorite_languages.items():
    print(f"{name.title()}'s favorite language is {language.title()}.")
    #        ^--^                                  ^------^
#     Jen's favorite language is Python.
#     Sarah's favorite language is C.
#     Edward's favorite language is Ruby.
#     Phil's favorite language is Python.
# }}}1

# The `keys()` method lets you iterate over the keys of a dictionary. {{{1

#                             v-----v
for name in favorite_languages.keys():
    print(name.title())
#     Jen
#     Sarah
#     Edward
#     Phil
#
#   But it can be omitted. {{{1

#                            no keys()
#                            v
for name in favorite_languages:
    print(name.title())
#     Jen
#     Sarah
#     Edward
#     Phil

#   The key variable can be used in the bracket notation to get the associated value. {{{1

friends = ['phil', 'sarah']
for name in favorite_languages:
    print(f'Hi {name.title()}.')

    if name in friends:
        #                            v----v
        language = favorite_languages[name].title()
        print(f'\t{name.title()}, I see you love {language}!')
#     Hi Jen.
#     Hi Sarah.
#             Sarah, I see you love C!
#     Hi Edward.
#     Hi Phil.
#             Phil, I see you love Python!
#
# More generally, any expression can be  used inside the brackets, provided that
# it evaluates to a string matching a key in the dictionary.
#
#   `keys()` is not limited to iterations.  It returns a list of keys which can be used however you like. {{{1

#                                  v-----v
if 'erin' not in favorite_languages.keys():
    print('Erin, please take our poll!')
#     Erin, please take our poll!
#
# Here, we don't iterate  over anything; we merely test the  presence of an item
# ('erin') inside the keys of the `favorite_languages` dictionary.
# }}}1

# Since Python 3.7, the items order is preserved when printing or iterating over a dictionary. {{{1

d = {
    'b': 2,
    'c': 3,
    'a': 1,
}

print(d)
#     {'b': 2, 'c': 3, 'a': 1}

for key, value in d.items():
    print(f'key = {key}, value = {value}')
#     key = b, value = 2
#     key = c, value = 3
#     key = a, value = 1

#   But `sorted()` lets you use a different order. {{{1

#           v----v
for name in sorted(favorite_languages):
    print(f'{name.title()}, thank you for taking the poll.')
#     Edward, thank you for taking the poll.
#     Jen, thank you for taking the poll.
#     Phil, thank you for taking the poll.
#     Sarah, thank you for taking the poll.
#
# The sentences are sorted alphabetically thanks to `sorted()`.

for name in favorite_languages:
    print(f'{name.title()}, thank you for taking the poll.')
#     Jen, thank you for taking the poll.
#     Sarah, thank you for taking the poll.
#     Edward, thank you for taking the poll.
#     Phil, thank you for taking the poll.
#
# Without `sorted()`,  the sentences would be  printed in the same  order as the
# names in `favorite_languages`.
# }}}1

# The `values()` method lets you iterate over the values of a dictionary. {{{1

print('The following languages have been mentioned:')
#                                 v-------v
for language in favorite_languages.values():
    print(language.title())
#     The following languages have been mentioned:
#     Python
#     C
#     Ruby
#     Python

#   The `set()` function can turn a list (possibly with duplicates) into a set (whose items are by definition unique). {{{1
# This is useful for `values()` because the latter can return a list with duplicates.

#               vvv
for language in set(favorite_languages.values()):
    print(language.title())
#     Ruby
#     Python
#     C
#
# This time, `Python` is no longer printed twice, because `set()` has turned the
# list output by `values()` into a set.

#   A set expression can be written directly without `set()`. {{{1

#           v                               v
languages = {'python', 'ruby', 'python', 'c'}
print(type(languages))
print(languages)
#     <class 'set'>
#     {'c', 'ruby', 'python'}
#
# A set is  surrounded by curly brackets, and duplicate  items are automatically
# removed (here the second `python` was removed).

#   A set is not ordered. {{{1
# Which differs from a dictionary and a list which *are* ordered.

s = {'a', 'b', 'c'}
print(s)
#     {'b', 'a', 'c'}
