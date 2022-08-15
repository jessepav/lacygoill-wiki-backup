# Purpose: use the list comprehension syntax to generate arbitrary list of numbers
# Reference: page 59 (paper) / 97 (ebook)

# The general syntax is:{{{
#
#     [<expression> for <variable> in <iterable> if <condition> == True]
#
# `<variable>` iterates over the values in `<iterable>`.
# Each value is used to replace `<variable>` inside `<expression>`.
# Each result is included in the final list.
#}}}
squares = [value ** 2 for value in range(1, 11)]
print(squares)
#     [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
