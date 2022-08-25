# Purpose: pass arguments to a function in various ways
# Reference: page 131 (paper) / 169 (ebook)

# To pass arguments to a function, we can use positional arguments. {{{1

def describe_pet(animal_type, pet_name):
    """Display information about a pet."""
    print(f'\nI have a {animal_type}.')
    print(f"My {animal_type}'s name is {pet_name.title()}.")

#            v-------v  v-----v
describe_pet('hamster', 'harry')
describe_pet('dog', 'willie')
#     I have a hamster.
#     My hamster's name is Harry.
#
#     I have a dog.
#     My dog's name is Willie.
#
# Here, `"hamster"` and  `"harry"` are both positional arguments,  which need to
# be specified in the correct order for the function to work as expected.

#   Or keyword arguments. {{{1

# A keyword argument  has the form `name=value`,  where `name` is the  name of a
# parameter and `value` is a value which you want to assign to that parameter.

def describe_pet(animal_type, pet_name):
    """Display information about a pet."""
    print(f'\nI have a {animal_type}.')
    print(f"My {animal_type}'s name is {pet_name.title()}.")

#            v-------------------v  v--------------v
describe_pet(animal_type='hamster', pet_name='harry')
#     I have a hamster.
#     My hamster's name is Harry.

# Here,   `animal_type='hamster'`  and   `pet_name='harry'`  are   both  keyword
# arguments; they assign the strings `"hamster"` and `"harry"` to the parameters
# `animal_type` and `pet_name`.

describe_pet(pet_name='harry', animal_type='hamster')
#     I have a hamster.
#     My hamster's name is Harry.
#
# Contrary  to  positional  arguments,  the  order in  which  you  pass  keyword
# arguments does not matter.  Which is why here, we get the same expected result
# as with  the previous function call;  even though we've reversed  the order of
# the arguments, which no longer matches the order of the parameters in function
# header.

#     You can mix positional and keyword arguments, but the latter must come last. {{{1

def func(a, b):
    pass

#        ✔
#       vvv
func(1, b=2)

#     ✘
#    vvv
func(b=2, 1)
#     SyntaxError: positional argument follows keyword argument˜
# }}}1

# You can make an argument optional by assigning a default value to its parameter. {{{1

# `animal_type='dog'` is not a keyword argument.{{{
#
# A keyword argument can only be used in a function call.
# We're not in a function *call*; we're in a function *header*.
#}}}
# `='dog'` assigns a default value to the parameter `animal_type`.{{{
#
# This lets  us omit a  value for `animal_type` in  a function call;  without an
# explicit value, the function will fall back on the default value `"dog"`.
#}}}
# We had to reverse the order of the parameters.{{{
#
# That's  because optional  parameters must  be declared  *after* the  mandatory
# ones.  And here, `pet_name` is mandatory  (you can't omit its argument), while
# `animal_type` is optional  (you *can* omit its argument thanks  to the default
# value `"dog"`).
#}}}
#                                     v----v
def describe_pet(pet_name, animal_type='dog'):
    """Display information about a pet."""
    print(f'\nI have a {animal_type}.')
    print(f"My {animal_type}'s name is {pet_name.title()}.")

# That's not a default value.{{{
#
# The latter is specific to a function header.
# We're not in a function header; we're in a function call.
#}}}
#                    v-------v
describe_pet(pet_name='willie')
#     I have a dog.
#     My dog's name is Willie.
#        ^^^
#
# Notice that no error  was given even though we didn't specify  a value for the
# second argument `animal_type`.   That's because we assigned  the default value
# `"dog"`.  Without, an error would have been given:
#
#     TypeError: describe_pet() missing 1 required positional argument: 'animal_type'

#                              v-------------------v
describe_pet(pet_name='harry', animal_type='hamster')
#     I have a hamster.
#     My hamster's name is Harry.
#        ^-----^
#
# This time,  the default  value `"dog"`  has been ignored,  because we  did not
# omit  the  argument for  `animal_type`;  we've  specified the  explicit  value
# `"hamster"`.

# If you don't provide the correct number of arguments, a traceback will be printed. {{{1
# Learning how to read it is useful to debug issues.

def describe_pet(animal_type, pet_name):
    """Display information about a pet."""
    print(f'\nI have a {animal_type}.')
    print(f"My {animal_type}'s name is {pet_name.title()}.")

describe_pet()
#     Traceback (most recent call last):
#       File "/path/to/script.py", line 10, in <module>
#       ^-----------------------^  ^------------------^
#                   A                       B
#         describe_pet()
#         ^------------^
#               C
#     TypeError: describe_pet() missing 2 required positional arguments: 'animal_type' and 'pet_name'
#     ^---------------------------------------------------------------------------------------------^
#                                                    D
#
# "A" gives us the name of the file where the line causing the error can be found.
#
# "B" gives us the absolute address of that line.
# The  "in <module>"  part means  that  the error  comes  from a  line which  is
# executed at the script  level; if it was inside a  function, the message would
# have been "in func" instead.  The line  number is always relative to the start
# of the script; regardless of whether "in <module>" or "in func" is reported.
#
# "C" gives us the contents of that line.
#
# "D" tells us the cause of the error.  Here, the function call `describe_pet()`
# is  missing  "2  required  positional arguments"  (aka  mandatory  arguments).
# Python has even looked at the definition  of the function to extract the names
# of the parameters `animal_type` and `pet_name`.
