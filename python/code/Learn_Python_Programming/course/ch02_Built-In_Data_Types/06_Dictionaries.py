# Purpose: work with dictionaries
# Reference: page 98

D = {'a': 1, 'b': 2, 'c': 3}

# Creation {{{1
# `{'key': value, ...}` {{{2

a = {'A': 1, 'Z': -1}

# `dict(**kwargs)` {{{2

# `dict()` accepts keyword  arguments which it packs into  a dictionary assigned
# to the  parameter for  the variadic keyword  arguments. `dict()`  returns that
# dictionary.
b = dict(A=1, Z=-1)
#        ^^^  ^--^
#        2 keyword arguments

# `dict(iterable)` {{{2
# `zip()` {{{3

# `zip()` expects variadic iterables:{{{
#
#     zip(*iterables)
#
# It  returns an  iterator which  yields tuples  until one  of the  iterables is
# exhausted.   The  i-th  tuple  is  constructed with  the  i-th  items  of  the
# iterables.
#}}}
z = zip('abcdefg', range(3), range(4))

# The  iterator returned  by `zip()`  can  be passed  to a  constructor such  as
# `list()` to build a list:
print(list(z))
#     [('a', 0, 0), ('b', 1, 1), ('c', 2, 2)]
#      ^---------^  ^---------^  ^---------^
#       1st yield    2nd yield     3 yield
#       1st items    2nd items     3rd items
#
# The shortest  iterable was `range(3)`  which is why  the list only  contains 3
# items. `range(3)` was exhausted before `range(4)` and "abcdefg".

# `dict(zip())` {{{3

# `dict()` is another constructor which builds dictionaries.
# Like other constructors (e.g. `list()`,  `set()`, ...), it accepts an iterable
# as argument.  It  accepts `zip()` because the latter gives  an iterator, which
# is a special kind of iterable  (it implements `__next__()`).  When it receives
# one, it builds a dictionary like this (and returns it):
#
#     d = {}
#     for k, v in iterable:
#         d[k] = v
#
# This assumes that the items of the iterable are containers holding 2 items.
c = dict(zip(['A', 'Z'], [1, -1]))

# `dict([('key', value), ...])` {{{3

d = dict([('A', 1), ('Z', -1)])

# `dict(dict)` {{{3

# `dict()` leaves a dictionary unchanged:
e = dict({'Z': -1, 'A': 1})
# }}}2
# all the same {{{2

print(a == b == c == d == e)
#     True
# }}}1
# Key-pair adding {{{1

D = {}

# The syntax to add a key-pair into a dictionary is `dict['key'] = value`:
D['a'] = 1
D['b'] = 2
print(D)
#     {'a': 1, 'b': 2}

# `dict['key']`  is  not limited  to  an  lvalue; it  can  also  be used  as  an
# expression to retrieve the value bound to a key:
print(D['a'])
#     1

# Key-pair removal {{{1

# The `del` statement deletes a key-pair from a dictionary (just like it deletes
# an item from a list):
del D['a']
print(D)
#     {'b': 2, 'c': 3}

# The `clear()` method makes a dictionary empty:
D.clear()
print(D)
#     {}

# Key membership test {{{1

# The `in`  and `not in` operator test  the presence and  absence of a key  in a
# dictionary:
print('c' in D)
print('e' not in D)
#     True
#     False

# But they cannot test the presence or absence of a value:
print(3 in D)
#     False

# length {{{1

# `len()` gives the number of key-pairs inside a dictionary:
print(len(D))
#     3
#
# It also works with strings and lists, and more generally with most objects.

