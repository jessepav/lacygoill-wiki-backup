# Purpose: Make a list  of the numbers from  one to one million, and  then use a
# `for` loop to print the numbers.  If the output is taking too long, stop it by
# pressing CTRL-C or by closing the output window.

# Reference: page 60 (paper) / 98 (ebook)

numbers = range(1, 10 ** 6 + 1)
for n in numbers:
    print(n)
