# Purpose: work with mutable sequences
# Reference: page 90

from math import prod
from operator import itemgetter

a = [1, 2, 1, 3]
b = [1, 3, 5, 7]
c = [(5, 3), (1, 3), (1, 2), (2, -1), (4, 9)]
d = [1, 3, 5, 7]
e = [6, 7, 8]

# Methods which give a new list operate in-place, but not functions.{{{
#
# Functions always give a copy.
#
# Example:
#
#     >>> l = [3, 1, 2]
#     >>> l.sort()
#     >>> l
#     [1, 2, 3]
#
#     >>> l = [3, 1, 2]
#     >>> sorted(l)
#     [1, 2, 3]
#     >>> l
#     [3, 1, 2]
#}}}

# There are 3 types of mutable sequences:{{{
#
#    - lists
#    - byte arrays
#    - sets
#}}}

# Lists {{{1
# Creation {{{2
# Brackets {{{3

# The general syntax for a list is `[item, ...]`:
print([1, 2, 3])
#     [1, 2, 3]

# `list()` {{{3

# The `list()`  function produces  a list  from from  any iterable  (including a
# tuple or a string):
print(list((1, 3, 5, 7, 9)))
print(list('hello'))
#     [1, 3, 5, 7, 9]
#     ['h', 'e', 'l', 'l', 'o']

# List comprehension {{{3

# A  list comprehension  is  a  powerful functional  feature  which can  produce
# complex lists:
print([x + 5 for x in [2, 3, 4]])
#     [7, 8, 9]
#
# The closest syntax In Vim9 would use `map()`:
#
#     :vim9 echo [2, 3, 4]->map((_, n) => n  + 5)
# }}}2
# Methods {{{2
# `append()` {{{3

# The `append()` method adds an item at the end of a list:
a.append(13)
print(a)
#     [1, 2, 1, 3, 13]
#                  ^^

# `count()` {{{3

# The `count()` method gives the number of times a value appears in a list:
print(a.count(1))
#     2

# `extend()` {{{3

# The `extend()` method extends a list by another:
a.extend([5, 7])
print(a)
#     [1, 2, 1, 3, 5, 7]
#                  ^--^

# More generally, `extend()` can extend a list by any iterable; including a tuple:
b = [0]
b.extend((1, 2, 3))
print(b)
#     [0, 1, 2, 3]
#
# Or a string:
b.extend('hello')
print(b)
#     [0, 1, 2, 3, 'h', 'e', 'l', 'l', 'o']

# `index()` {{{3

# The `index()` method gives the index of an item in a list, specified by its value:
print(a.index(2))
#     1

# `insert()` {{{3

# The `insert()` method adds an item in a list at a given index:
a.insert(0, 17)
#        ^  ^^
#    index  item
print(a)
#     [17, 1, 2, 1, 3]
#      ^^

# `pop()` {{{3

# The `pop()` method removes and returns the last item from a list:
#
#       vvv
print(a.pop())
#     3

# The `pop()` method removes an item from a list, specified by its index.
#
#           index
#           v
print(a.pop(3))
print(a)
#     3
#     [1, 2, 1]

# `remove()` {{{3

# The `remove()` method removes an item from a list, specified by its value:
a.remove(2)
print(a)
#     [1, 1, 3]

# `reverse()` {{{3

# The `reverse()` method reverses the order of the items in a list:
a.reverse()
print(a)
#     [3, 1, 2, 1]

# `sort()` {{{3

# The `sort()` method sorts the order of the items in a list:
a.sort()
print(a)
#     [1, 1, 2, 3]

# `clear()` {{{3

# The `clear()` method removes all items in a list:
a.clear()
print(a)
#     []
# }}}2
# Functions {{{2
# `min()`, `max()` {{{3

# The `min()` and `max()` functions give the smallest and largest numbers in a list:
print(min(b))
print(max(b))
#     1
#     7

# `len()` {{{3

# The `len()` function gives the number of items in a list:
print(len(b))
#     4

# `sum()`, `prod()` {{{3

# The `sum()` and `prod()` functions give the sum and product of all numbers in a list:
print(sum(b))
print(prod(b))
#     16
#     105

# `sorted()` gives a sorted copy of a list.
# If the items  in that list are  sequences, the sorting is done  on their first
# item.   If 2  items have  the  same score,  then the  2nd  item is  used as  a
# tie-breaker (and the process can repeat itself):
print(sorted(c))
#     [(1, 2), (1, 3), (2, -1), (4, 9), (5, 3)]

# `sorted()` {{{3
# `itemgetter()` {{{4

# `sorted()` accepts  a keyword  argument, `key=itemgetter(...)`, which  is only
# valid if the list items are sequences.
# `itemgetter()` expects the index of the item inside the sequences on which the
# sorting should be done:
#
#               v---------------v
print(sorted(c, key=itemgetter(0)))
#     [(1, 3), (1, 2), (2, -1), (4, 9), (5, 3)]

# `itemgetter()` accepts several arguments; the 2nd  one (and beyond) is used as
# a tie-breaker:
#
#                                 v
print(sorted(c, key=itemgetter(0, 1)))
#     [(1, 2), (1, 3), (2, -1), (4, 9), (5, 3)]
#
# This time,  `(1, 2)` comes  before `(1, 3)`, because  even though  both tuples
# score the  same according to their  first item, they don't  according to their
# second item.

# We could also ignore the first item entirely, and only sort on the second one:
print(sorted(c, key=itemgetter(1)))
#     [(2, -1), (1, 2), (5, 3), (1, 3), (4, 9)]

# `reverse=True` {{{4

# `sorted()`  also accepts  an optional  `reverse=True` keyword  argument, whose
# effect is to reverse the order of the sorting.
#
#                                  v----------v
print(sorted(c, key=itemgetter(1), reverse=True))
#     [(4, 9), (5, 3), (1, 3), (1, 2), (2, -1)]

# More generally, those functions work on any iterable.
# And `len()` works on any object.
# }}}2
# Operators {{{2

# The `+` operator concatenates sequences:
#
#       v
print(d + e)
#     [1, 3, 5, 7, 6, 7, 8]
#      ^--------^  ^-----^
#          d          e

# The `*` operator repeats a sequence an arbitrary number of times:
#
#       v
print(d * 3)
#     [1, 3, 5, 7, 1, 3, 5, 7, 1, 3, 5, 7]
#      ^--------^  ^--------^  ^--------^
#          1           2           3
# }}}1
# Byte arrays {{{1
# Creation {{{2

# `bytearray()` produces an empty byte array:
print(bytearray())
#     bytearray(b'')

# It accepts an optional argument to repeat the null byte:
#
#               vv
print(bytearray(10))
#     bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

# It accepts an optional iterable yielding integers in `range(256)`:
#
#               v------v
print(bytearray(range(5)))
#     bytearray(b'\x00\x01\x02\x03\x04')
#
# Here, the  bytes have  increasing values  because `range()`  yields increasing
# integers.

# It accepts an optional bytes object:
#
#               v------v
print(bytearray(b'bytes'))
#     bytearray(b'bytes')
#
# The result is the same bytes sequence, except that it's mutable.

# Methods {{{2

# A byte array supports most methods which work on strings, and most methods which work on lists.

name = bytearray(b'Lina')

print(name.replace(b'L', b'l'))
#     bytearray(b'lina')

print(name.endswith(b'na'))
#     True

print(name.lower())
print(name.upper())
#     bytearray(b'lina')
#     bytearray(b'LINA')

print(name.count(b'L'))
#     1

# The methods seen thus far don't operate in-place; they produce a new copy.
# That's because they can also be invoked on strings which are immutable.

# But, `append()` does operate in-place:
#
#           vvv
name.append(100)
print(name)
#     bytearray(b'Linad')
#                     ^
#
# That's because it can also be invoked on lists which *are* mutable.
# }}}1
# Sets {{{1
# Creation {{{2

# A set can be created with the `{...}` syntax:
s = {2, 3, 5, 5, 3}
print(s)
#     {2, 3, 5}
#
# `5` was not included twice, even though it was specified twice.
# That's because a set cannot include duplicate items.

# And with the `set()` function:
s = set()
# Without any argument, `set()` gives an empty set.

# `set()` accepts any iterable as an argument:
print(set(range(1, 4)))
print(set([4, 5, 6]))
#     {1, 2, 3}
#     {4, 5, 6}

# Methods {{{2
# Sets support some methods which also work on lists.

small_primes = set()

# The `add()` method adds items in a set:
small_primes.add(2)
small_primes.add(3)
small_primes.add(5)
print(small_primes)
#     {2, 3, 5}

# let's add a *non*-prime number to have a reason to remove an item
small_primes.add(1)
print(small_primes)
#     {1, 2, 3, 5}

# The `remove()` method removes an item from a set:
small_primes.remove(1)
print(small_primes)
#     {2, 3, 5}

# Operators {{{2
# Common with lists {{{3

# The `in` membership operator tests whether a given value is in a given set:
print(3 in small_primes)
print(4 in small_primes)
#     True
#     False

# The `not in` membership operator tests whether a given value is *not* in a given set:
print(4 not in small_primes)
#     True

# Specific to sets {{{3

small_primes = {2, 3, 5}
bigger_primes = {5, 7, 11, 13}

# The `|` operator computes the *union* between 2 sets:
#                  v
print(small_primes | bigger_primes)
#     {2, 3, 5, 7, 11, 13}

# The `&` operator computes the *intersection* between 2 sets:
#                  v
print(small_primes & bigger_primes)
#     {5}

# The `-` operator computes the *difference* between 2 sets:
#                  v
print(small_primes - bigger_primes)
#     {2, 3}
