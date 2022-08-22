# Purpose: Put the `print_models()` and `show_completed_models()` functions in a
# separate file called `printing_functions.py`.   Write an `import` statement at
# the top of this file and use the imported functions.

# Reference: page 155 (paper) / 193 (ebook)

# ----------------------------v
import printing_functions as pf

unprinted_designs = ['phone case', 'robot pendant', 'dodecahedron']
completed_models = []
pf.print_models(unprinted_designs[:], completed_models)
pf.show_completed_models(completed_models)
print('\n' + str(unprinted_designs))
#     Printing model: dodecahedron
#     Printing model: robot pendant
#     Printing model: phone case
#
#     The following models have been printed:
#     dodecahedron
#     robot pendant
#     phone case
#
#     ['phone case', 'robot pendant', 'dodecahedron']
