# Purpose: reverse sort order of a list
# Reference: page 45 (paper) / 83 (ebook)

# To  reverse the  order in  which the  items  of a  list are  indexed, use  the
# `reverse()` method.
cars = ['bmw', 'audi', 'toyota', 'subaru']
print(cars)
cars.reverse()
#   ^------^
print(cars)
#     ['bmw', 'audi', 'toyota', 'subaru']
#     ['subaru', 'toyota', 'audi', 'bmw']
#
# Just like `sort()`, `reverse()` operate in-place.
# But contrary to `sort()` for which an alternative exists to preserve the order
# of the  original list  (the `sorted()` function),  `reverse()` has  no similar
# alternative.  Although, you can:
#
#    - make a copy of the list first, and reverse that copy
#    - reverse the list a 2nd time, to cancel the effect of the first call to
#      `reverse()`
