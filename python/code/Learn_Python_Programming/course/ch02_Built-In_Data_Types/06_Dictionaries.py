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
# `dict(zip(...))` {{{3

# `dict()` is a constructor which builds dictionaries.{{{
#
# Like other constructors (e.g. `list()`,  `set()`, ...), it accepts an iterable
# as argument.  It  accepts `zip()` because the latter gives  an iterator, which
# is a special kind of iterable  (it implements `__next__()`).
# `dict()` exhausts `zip()`  into a sequence of tuples, builds  a dictionary out
# of them (by binding their items as key-value pairs), and returns it:
#
#     d = {}
#     for k, v in iterable:
#         d[k] = v
#
# This assumes  that the items  of the iterable  are containers holding  2 items
# (otherwise, the built dictionary would be empty).
#}}}
c = dict(zip(['A', 'Z'], [1, -1]))

print(dict(zip('hello', range(5))))
#     {'h': 0, 'e': 1, 'l': 3, 'o': 4}
#
# The order in which the items were added into the dictionary has been preserved.{{{
#
# The  fact that  we  can read  "helo"  by iterating  over the  keys  is not  an
# accident:  Dictionary order  is guaranteed to be insertion  order since Python
# 3.7.
#}}}
# "l" is associated to 3, not 2.{{{
#
# That's because "hello" contains 2 "l" characters.
# The first "l" was associated to 2, and the second "l" to 3.
# But a  key can only be  associated to a  single value, which implies  that the
# last  tuple  with an  "l"  wins  (its  value  overwrites the  value  currently
# associated).
#}}}

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
# Key-value pair adding {{{1

d = {}

# The syntax to add a key-value pair into a dictionary is `dict['key'] = value`:
d['a'] = 1
d['b'] = 2
print(d)
#     {'a': 1, 'b': 2}

# `dict['key']`  is  not limited  to  an  lvalue; it  can  also  be used  as  an
# expression to retrieve the value associated to a key:
print(d['a'])
#     1

# Key-value pair removal {{{1

# The `del` statement  deletes a key-value pair from a  dictionary (just like it
# deletes an item from a list):
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

# dictionary views {{{1

d = {'a': 1, 'b': 2, 'c': 3}

# Key view:
print(d.keys())
#     dict_keys(['a', 'b', 'c'])

# Items view:
print(d.items())
#     dict_items([('a', 1), ('b', 2), ('c', 3)])

# A dictionary view supports membership tests:
print(3 in d.values())
print(('b', 2) in d.items())
#     True
#     True

# `len()` {{{1

# `len()` gives the number of key-value pairs inside a dictionary:
print(len(D))
#     3
#
# It also works with strings and lists, and more generally with most objects.

# `reversed()` {{{1

# Since Python 3.8, dictionaries are reversible:
print(list(reversed(D)))
#     ['c', 'b', 'a']

# `pop()`, `popitem()` {{{1

# `pop()` removes a key, and returns its value:
print(D.pop('b'))
#     2

# If the key does not exist, `KeyError` is raised:
#
#     E.pop('not-a-key')
#     KeyError: 'not-a-key'˜

# Unless, you pass a second optional argument, which is then used as a default value:
print(D.pop('not-a-key', 'default-value'))
#     default-value

# `popitem()` removes and returns a (key, value) pair as a 2-tuple:
print(D.popitem())
print(D)
#     ('c', 3)
#     {'a': 1}
#
# Pairs are returned in LIFO order (last-in, first-out).

# `update()` {{{1

# `update()` adds key-value pairs into a dictionary.
# They  can be  be  specified with  a single  dictionary  argument, and/or  with
# variadic keyword arguments:
D.update({'another': 'value'})
D.update(a=13)
print(D)
#     {'a': 13, 'b': 2, 'c': 3, 'another': 'value'}
#      ^-----^                  ^----------------^
#      updated item                 added item

# `get()` {{{1

# `get()` returns the  value for a key,  without giving an error if  it does not
# exist.  In that case,  it defaults to its 2nd argument,  which is optional and
# defaults to `None`:
print(D.get('a'))
print(D.get('a', 177))
print(D.get('x', 177))
print(D.get('x'))
#     1
#     1
#     177
#     None

# `setdefault()` {{{1

d = {}

# `setdefault()` is similar to `get()`.
# It retrieves  the value  associated to a  given key, and  defaults to  its 2nd
# optional argument if the  key doesn't exist (or to `None`  if that argument is
# missing).
# However, if the key doesn't exist, `setdefault()` also adds the key-value pair
# value inside the dictionary (`get()` doesn't do that).
print(d.setdefault('a', 1))
print(d)
#     1
#     {'a': 1}
#
# The dictionary has changed: it now contains the key-value pair `(a, 1)`.

print(d.setdefault('a', 5))
print(d)
#     1
#     {'a': 1}
#
# The dictionary has  *not* changed, because the `a` key  already existed at the
# time `setdefault()` was invoked a 2nd time.


# Calls to `setdefault()` can be chained (like all methods):
d = {}
d.setdefault('a', {}).setdefault('b', []).append(1)
print(d)
#     {'a': {'b': [1]}}
#
# Explanation:{{{
#
# The first call to `setdefault()` adds the key-value pair `(a, {})`:
#
#     d = {'a': {}}
#          ^-----^
#
# And it returns the added value `{}`.
# The second  call to `setdefault()`  adds the  key-value pair `(b, [])`  to the
# previously returned value `{}`:
#
#     d = {'a': {'b': []}}
#                ^-----^
#
# Finally, the call to `append()` adds 1 to the previously returned value `[]`:
#
#     d = {'a': {'b': [1]}}
#                      ^
#}}}
# union {{{1

d = {'a': 'A', 'b': 'B'}
e = {'b': 8, 'c': 'C'}

# The `|` operator computes the union of 2 dictionaries (require Python 3.9):
print(d | e)
print(e | d)
#     {'a': 'A', 'b': 8, 'c': 'C'}
#     {'b': 'B', 'c': 'C', 'a': 'A'}
#
# The results are different, even though the operands are the same.
# That's because the union operation is not commutative for dictionaries (but it
# is  for sets).  If the  dictionaries have a  key in common but  with different
# values, the value in the last operand overrides the other.

# Unpacking a  dictionary inside curly  brackets is  another way to  compute the
# union of 2 dictionaries:
print({**d, **e})
print({**e, **d})
#     {'a': 'A', 'b': 8, 'c': 'C'}
#     {'b': 'B', 'c': 'C', 'a': 'A'}

# The augmented  assignment operator `|=`  computes the union of  2 dictionaries
# and assigns it to the operand in its LHS:
d |= e
print(d)
#     {'a': 'A', 'b': 8, 'c': 'C'}
