# Purpose: remove an item from a list
# Reference: page 38 (paper) / 76 (ebook)

# You can remove an item from a list using the `del` statement. {{{1

# This assumes that you know the index of the item:
motorcycles = ['honda', 'yamaha', 'suzuki']
print(motorcycles)
del motorcycles[1]
print(motorcycles)
#     ['honda', 'yamaha', 'suzuki']
#     ['honda', 'suzuki']

# If you want to remove an item *and* do something with its value, use the `pop` method instead. {{{1

# The latter  accepts an optional index  argument which defaults to  `-1`.  IOW,
# without any argument `pop()` removes and returns the last item of a list.
motorcycles = ['honda', 'yamaha', 'suzuki']
print(motorcycles)
last_owned = motorcycles.pop()
#                       ^----^
print(motorcycles)
print(f'The last motorcycle I owned was a {last_owned.title()}.')
first_owned = motorcycles.pop(0)
#                        ^-----^
print(motorcycles)
print(f'The first motorcycle I owned was a {first_owned.title()}.')
#     ['honda', 'yamaha', 'suzuki']
#     ['honda', 'yamaha']
#     The last motorcycle I owned was a Suzuki.
#     ['yamaha']
#     The first motorcycle I owned was a Honda.

# The `remove()` methods lets you remove an item by specifying its value rather than its index. {{{1

# And just  like `pop()`,  it also  returns the value  which you  can save  in a
# variable to refer to it later in your code.
motorcycles = ['honda', 'yamaha', 'suzuki', 'ducati']
too_expensive = 'ducati'
motorcycles.remove(too_expensive)
#          ^-----^
print(motorcycles)
print(f'A {too_expensive.title()} is too expensive for me.')
#     ['honda', 'yamaha', 'suzuki']
#     A Ducati is too expensive for me.
#
# Note that `remove()` only removes the first occurrence of the value.
# If the  list contains  the same value  at different indexes,  and you  want to
# remove all of them, you'll need to call `remove()` once for each.
