# Purpose: assign a value to a variable
# Reference: page 16 (paper) / 54 (ebook)

# Usage example of a variable: {{{1

# variable name
# ----v
message = 'Hello Python world!'
#         ^-------------------^
#                 value
print(message)

# You can change the value of a variable in your program at any time. {{{1

# Python will always keep track of its current value.
message = 'Hello Python Crash Course world!'
print(message)

# A variable name can only contain letters, numbers, and underscores. {{{1

# it can start with an underscore
_message = 'valid variable name'
print(_message)

# but not with a number
1_message = 'invalid variable name'
print(message)
#     SyntaxError: invalid decimal literal

# and it can't conflict with a keyword
if = 'value'
#     SyntaxError: invalid syntax

# nor with a function name
print = 'value'
print(print)
#     TypeError: 'str' object is not callable
