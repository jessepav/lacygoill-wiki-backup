# Purpose: import all items from a module, directly in the namespace of the current script
# Reference: page 153 (paper) / 191 (ebook)

from pizza import *
#                 ^
#
# The asterisk is used some kind of wildcard to match any item from the module `pizza`.
# **But unless you have a good reason to do so, don't use this syntax.**
# **See `pitfalls.md`.**

# We don't  need to prefix `make_pizza()`  with any module name,  because it was
# imported in the current namespace.
make_pizza(16, 'pepperoni')
make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')
#     Making a 16-inch pizza with the following toppings:
#     - pepperoni
#
#     Making a 12-inch pizza with the following toppings:
#     - mushrooms
#     - green peppers
#     - extra cheese
