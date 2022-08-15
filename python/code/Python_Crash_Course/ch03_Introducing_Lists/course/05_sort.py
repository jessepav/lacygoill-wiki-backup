# Purpose: sort a list
# Reference: page 43 (paper) / 81 (ebook)

# The `sort()` method can be called to sort a list in-place. {{{1

cars = ['bmw', 'audi', 'toyota', 'subaru']
cars.sort()
#   ^---^
print(cars)
#     ['audi', 'bmw', 'subaru', 'toyota']

#   It accepts an optional `reverse=True` argument to reverse the sort order. {{{1

cars = ['bmw', 'audi', 'toyota', 'subaru']
cars.sort(reverse=True)
#         ^----------^
print(cars)
#     ['toyota', 'subaru', 'bmw', 'audi']
#}}}1

# If you don't want to change the original list, but just get an ordered copy, use the `sorted()` function. {{{1

cars = ['bmw', 'audi', 'toyota', 'subaru']
print('Here is the original list:')
print(cars)
print('\nHere is the sorted list:')
print(sorted(cars))
#     ^----^
print('\nHere is the original list again:')
print(cars)
#     Here is the original list:
#     ['bmw', 'audi', 'toyota', 'subaru']
#
#     Here is the sorted list:
#     ['audi', 'bmw', 'subaru', 'toyota']
#
#     Here is the original list again:
#     ['bmw', 'audi', 'toyota', 'subaru']

#   Just like `sort()` the method, the `sorted()` function also accepts an optional `reverse=True` argument. {{{1

cars = ['bmw', 'audi', 'toyota', 'subaru']
print('\nHere is the original list:')
print(cars)
print('\nHere is the sorted list:')
print(sorted(cars, reverse=True))
#                  ^----------^
print('\nHere is the original list again:')
print(cars)
