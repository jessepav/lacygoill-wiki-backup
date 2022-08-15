# Purpose: introducing type hints
# Reference: page 37 (paper) / 58 (ebook)


# Code and data is an object in Python.
# Even a simple string or number.
print(type('Hello, world!'))
#     <class 'str'>
#
# The string 'Hello, world!' is an instance of the built-in class `str`.

print(type(42))
#     <class 'int'>
#
# The number 42 is an instance of the built-in class `int`.


# A type information is not attached to a variable, but to an object.
a_string_variable = 'Hello, world!'
print(type(a_string_variable))
#     <class 'str'>
a_string_variable = 42
print(type(a_string_variable))
#     <class 'int'>
#
# Notice that the type of `a_string_variable` can change depending on what value
# it's being assigned.
# That's  because a  variable  doesn't have  a  type  of its  own;  it's just  a
# reference to an object.
