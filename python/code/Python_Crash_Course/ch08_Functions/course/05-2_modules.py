# Purpose: import some item from a module
# Reference: page 152 (paper) / 190 (ebook)

# You can import specific items from a module.

from pizza import make_pizza
# -------------------------^
# Only import the `make_pizza()` function from the `pizza` module.
# We could import more items from the module:
#
#     from pizza import make_pizza, another_item, yet_another_item, ...
#                                   ^----------^  ^--------------^

# Notice that this time, you don't need to prefix the function `make_pizza()` with the module `pizza`.{{{
#
#     pizza.make_pizza(16, 'pepperoni')
#     ^----^
#       ✘
#
# Rationale: Since you only  import specific items, provided that  you don't use
# one of their names for an item  defined in this script, you have the guarantee
# to avoid any collision.
#}}}
make_pizza(16, 'pepperoni')
make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')
#     Making a 16-inch pizza with the following toppings:
#     - pepperoni
#
#     Making a 12-inch pizza with the following toppings:
#     - mushrooms
#     - green peppers
#     - extra cheese
