# Purpose: import some item from a module and give it an alias
# Reference: page 152 (paper) / 190 (ebook)

# You can give an alias to an imported item.

from pizza import make_pizza as mp
#                            ^---^
#
# This syntax lets you access an item under a different name.
# Here, we use it to shorten the name of `make_pizza()` into `mp()`.
# In general,  it's useful  to avoid  a collision  with an  item in  the current
# script, which we can't or don't want to rename.

mp(16, 'pepperoni')
mp(12, 'mushrooms', 'green peppers', 'extra cheese')
#     Making a 16-inch pizza with the following toppings:
#     - pepperoni
#
#     Making a 12-inch pizza with the following toppings:
#     - mushrooms
#     - green peppers
#     - extra cheese
