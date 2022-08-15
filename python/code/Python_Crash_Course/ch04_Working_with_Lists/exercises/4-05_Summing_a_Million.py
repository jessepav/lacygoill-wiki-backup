# Purpose: Make a  list of  the numbers from  one to one  million, and  then use
# `min()` and `max()` to make sure your  list actually starts at one and ends at
# one million.  Also, use the `sum()` function to see how quickly Python can add
# a million numbers.

# Reference: page 60 (paper) / 98 (ebook)

numbers = range(1, 10 ** 6 + 1)
print(min(numbers))
print(max(numbers))
print(sum(numbers))
#     1
#     1000000
#     500000500000
