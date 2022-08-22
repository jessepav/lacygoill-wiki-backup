# Purpose: import a module and give it an alias
# Reference: page 153 (paper) / 191 (ebook)

# You can give an alias to an imported module.
# It's useful to make a long module name less verbose.

import pizza as p
#            ^--^

p.make_pizza(16, 'pepperoni')
p.make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')
#     Making a 16-inch pizza with the following toppings:
#     - pepperoni
#
#     Making a 12-inch pizza with the following toppings:
#     - mushrooms
#     - green peppers
#     - extra cheese
