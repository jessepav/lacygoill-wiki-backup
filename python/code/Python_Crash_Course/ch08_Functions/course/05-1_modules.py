# Purpose: import all items from a module, in a separate namespace
# Reference: page 150 (paper) / 188 (ebook)

# Importing lets us use items (functions, constants, ...) from a different script.


# You can import a module as a whole.

# This  `import`  statement tells  Python  to  make  the items  from  `pizza.py`
# available in this script.  In particular, we want its `make_pizza()` function.
import pizza
# ---------^
# Notice that we must drop the `.py` file extension.

# Since `make_pizza()` is not defined in this script, you need to prefix it with the name of its module.{{{
#
# Rationale: Since  you don't  know  in advance  all the  items  defined in  the
# module, without  a separate namespace  you would  have no guarantee  against a
# collision between an imported item and an  item in the current script with the
# same name.
#}}}
# ---v
pizza.make_pizza(16, 'pepperoni')
pizza.make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')
#     Making a 16-inch pizza with the following toppings:
#     - pepperoni
#
#     Making a 12-inch pizza with the following toppings:
#     - mushrooms
#     - green peppers
#     - extra cheese
