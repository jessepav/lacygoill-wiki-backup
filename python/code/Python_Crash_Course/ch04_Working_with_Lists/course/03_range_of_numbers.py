# Purpose: use the `range()` function to iterate over numerical lists
# Reference: page 57 (paper) / 95 (ebook)

# `range()` can generate a range of numbers which can be iterated over. {{{1

for value in range(1, 5):
    print(value)
    #     1
    #     2
    #     3
    #     4

# You might have expected `5` to be printed.
# That didn't happen because the 2nd argument of `range()` is exclusive.

# The first argument is optional.  If you omit it, `range()` starts from 0. {{{1
for value in range(5):
    print(value)
    #     0
    #     1
    #     2
    #     3
    #     4
#}}}1

# The output of `range()` is not a list. {{{1

print(range(1, 6))
#     range(1, 6)

# It has its own type:
print(type(range(1, 6)))
#     <class 'range'>

#   But you can turn its output into a list using the `list()` function. {{{1

numbers = list(range(1, 6))
print(numbers)
#     [1, 2, 3, 4, 5]
#}}}1

# `range()` accepts a 3rd optional argument (`step`). {{{1

# It's added to an output number to get the next one.
# It defaults  to 1, which is  why by default  you get a contiguous  sequence of
# integers.
even_numbers = list(range(2, 11, 2))
print(even_numbers)
#     [2, 4, 6, 8, 10]

# By iterating over a `range()`, we can build arbitrarily complex lists of numbers. {{{1

# For example, you could get the first 10 square numbers:
squares = []
for value in range(1, 11):
    square = value ** 2
    squares.append(square)

print(squares)
#     [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
