# Purpose: work with a tuple
# Reference: page 65 (paper) / 103 (ebook)

dimensions = (200, 50)

# syntax {{{1

# The main difference between a list  and a tuple expression are the surrounding
# braces.  We use parentheses for a tuple, instead of square brackets.
#            v       v
dimensions = (200, 50)
print(dimensions[0])
print(dimensions[1])
#     200
#     50

# A tuple must include at least 1 comma, even if it contains only 1 item. {{{1

print(type(3))
print(type((3,)))
#            ^
#     <class 'int'>
#     <class 'tuple'>

# A tuple is immutable, which means you can't add/remove/change any of its items. {{{1

dimensions[0] = 250
#     TypeError: 'tuple' object does not support item assignment

# You can iterate over a tuple, just like a list. {{{1

for dimension in dimensions:
    print(dimension)
#     200
#     50

# We can change the value of a tuple variable. {{{1

print('Original dimensions:')
for dimension in dimensions:
    print(dimension)
#     Original dimensions:
#     200
#     50

dimensions = (400, 100)
print('\nModified dimensions:')
for dimension in dimensions:
    print(dimension)
#     Modified dimensions:
#     400
#     100

# No error was raised because we didn't change the tuple itself.
# We changed a variable.
# The fact that this variable referred to a tuple is irrelevant.
# It is  allowed to change a  variable/reference (regardless of the  type of the
# object it currently refers to) so that it  refers to any other object; be it a
# number, a string, a list, or yet another tuple.
