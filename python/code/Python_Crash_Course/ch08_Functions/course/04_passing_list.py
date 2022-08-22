# Purpose: pass a list of arguments to a function in various ways
# Reference: page 143 (paper) / 181 (ebook)

# You can pass a list of arguments to a function by first packing them into a list. {{{1

def greet_users(names):
    """Print a simple greeting to each user in the list."""
    for name in names:
        msg = f'Hello, {name.title()}!'
        print(msg)

# -----------------------------------v
usernames = ['hannah', 'ty', 'margot']
#           v-------v
greet_users(usernames)
#     Hello, Hannah!
#     Hello, Ty!
#     Hello, Margot!

#   But lists are passed by reference, not by copy.  Pass a copy if you need the original unchanged. {{{1

# Making a copy  of a list costs time  and memory; and the bigger  the list, the
# bigger the  cost.  Only pass  a copy if  you really need  to; that is,  if the
# function makes the list mutate, and you need to keep the original value.

def print_models(unprinted_designs, completed_models):
    """
    Simulate printing each design, until none are left.
    Move each design to `completed_models` after printing.
    """
    while unprinted_designs:
        current_design = unprinted_designs.pop()
        print(f'Printing model: {current_design}')
        completed_models.append(current_design)

def show_completed_models(completed_models):
    """Show all the models that were printed."""
    print('\nThe following models have been printed:')
    for completed_model in completed_models:
        print(completed_model)

# Start with some designs that need to be printed.
unprinted_designs = ['phone case', 'robot pendant', 'dodecahedron']
completed_models = []

# We pass a copy of `unprinted_designs` so that the original value is preserved.
#                             vvv
print_models(unprinted_designs[:], completed_models)
show_completed_models(completed_models)
#     Printing model: dodecahedron
#     Printing model: robot pendant
#     Printing model: phone case
#
#     The following models have been printed:
#     dodecahedron
#     robot pendant
#     phone case

# Let's make sure that `unprinted_designs` has kept its original value.
print('\n' + str(unprinted_designs))
#     ['phone case', 'robot pendant', 'dodecahedron']
#
# It did.   If we  hadn't used  `[:]` to make  a copy  before passing  the list,
# the  latter would  be  empty now  (because  of the  `pop()`  method called  in
# `print_models()`).
# }}}1

# If you need to pass a variable number of arguments, which are unpacked, then use an `*args` parameter. {{{1

# There can  only be  1 `*args`  in a  function header;  it's the  parameter for
# variadic arguments.

# What matters is the `*` prefix, not the parameter's name.
#              v-------v
def make_pizza(*toppings):
    """Print the list of toppings that have been requested."""
    print(toppings)

make_pizza('pepperoni')
make_pizza('mushrooms', 'green peppers', 'extra cheese')
#     ('pepperoni',)
#     ('mushrooms', 'green peppers', 'extra cheese')
#     ^                                            ^
#
# The function has packed the list of arguments into tuples.

#   You can interact with the arguments like you would with any tuple. {{{1

# There can only  be 1 `**kwargs` in  a function header; it's  the parameter for
# variadic keyword arguments.

# For example, you can  iterate over its items to print  some message about each
# passed argument.

def make_pizza(*toppings):
    """Summarize the pizza we are about to make."""
    print('\nMaking a pizza with the following toppings:')
    # ---------------------v
    for topping in toppings:
        print(f'- {topping}')

make_pizza('pepperoni')
make_pizza('mushrooms', 'green peppers', 'extra cheese')
#     Making a pizza with the following toppings:
#     - pepperoni
#
#     Making a pizza with the following toppings:
#     - mushrooms
#     - green peppers
#     - extra cheese

# If you need to pass a variable number of *keyword* arguments, which are unpacked, then use a `**kwargs` parameter. {{{1

# Again, what matters is the `**` prefix, not the parameter's name.
#                              v---------v
def build_profile(first, last, **user_info):
    """Build a dictionary containing everything we know about a user."""
    user_info['first_name'] = first
    user_info['last_name'] = last
    return user_info

user_profile = build_profile('albert', 'einstein',
                             location='princeton',
                             field='physics')
print(user_profile)
#     {'location': 'princeton', 'field': 'physics', 'first_name': 'albert', 'last_name': 'einstein'}
#
# The function has packed the list of keyword arguments into a dictionary, which
# we've extended with the first 2 positional arguments.
# }}}1

# `*args` must come after mandatory parameters. {{{1

# `*toppings` is declared *after* the mandatory `size` parameter.
#              v-------------v
def make_pizza(size, *toppings):
    """Summarize the pizza we are about to make."""
    print(f'\nMaking a {size}-inch pizza with the following toppings:')
    for topping in toppings:
        print(f'- {topping}')

make_pizza(16, 'pepperoni')
make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')
#     Making a 16-inch pizza with the following toppings:
#     - pepperoni
#
#     Making a 12-inch pizza with the following toppings:
#     - mushrooms
#     - green peppers
#     - extra cheese

#   Exception: they can be declared before a certain kind of mandatory parameters (keyword-only). {{{1

# This time, `*toppings` is declared *before* the mandatory `size` parameter.
# But this causes `size` to no longer be a positional-or-keyword parameter; it's
# now a keyword-only parameter.  This means that  it can only be assigned with a
# keyword argument.
#              v-------------v
def make_pizza(*toppings, size):
    """Summarize the pizza we are about to make."""
    print(f'\nMaking a {size}-inch pizza with the following toppings:')
    for topping in toppings:
        print(f'- {topping}')

#                       v-----v
make_pizza('pepperoni', size=16)
make_pizza('mushrooms', 'green peppers', 'extra cheese', size=12)
#                                                        ^-----^
# A simple  positional argument  wouldn't work  here; we  need to  specify which
# parameter this argument is meant to be assigned to.
