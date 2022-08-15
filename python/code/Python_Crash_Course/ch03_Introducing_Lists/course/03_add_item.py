# Purpose: add an item into a list
# Reference: page 37 (paper) / 75 (ebook)

# To add an item at the end of a list, use the `append()` method. {{{1

motorcycles = ['honda', 'yamaha', 'suzuki']
print(motorcycles)
motorcycles.append('ducati')
#          ^------^
print(motorcycles)
#     ['honda', 'yamaha', 'suzuki']
#     ['honda', 'yamaha', 'suzuki', 'ducati']
#                                   ^------^

#   `append()` is useful to build a list dynamically at runtime. {{{1

motorcycles = []
motorcycles.append('honda')
motorcycles.append('yamaha')
motorcycles.append('suzuki')
print(motorcycles)
#     ['honda', 'yamaha', 'suzuki']
#}}}1

# To add an item at any position, use the `insert()` method. {{{1
motorcycles = ['honda', 'yamaha', 'suzuki']
motorcycles.insert(0, 'ducati')
print(motorcycles)
#     ['ducati', 'honda', 'yamaha', 'suzuki']
#
# Notice how all the  items after the added one are shifted  one position to the
# right.
