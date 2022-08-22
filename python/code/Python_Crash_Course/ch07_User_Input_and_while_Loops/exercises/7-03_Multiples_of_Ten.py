# Purpose: Ask the  user for a number,  and then report whether the  number is a
# multiple of 10 or not.

# Reference: page 117 (paper) / 155 (ebook)

n = int(input('number: '))
if n % 10 == 0:
    print(f'{n} is a multiple of 10.')
else:
    print(f'{n} is NOT a multiple of 10.')
#     number: 123
#     123 is NOT a multiple of 10.
