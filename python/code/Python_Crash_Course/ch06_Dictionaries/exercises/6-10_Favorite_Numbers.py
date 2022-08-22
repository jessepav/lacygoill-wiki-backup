# Purpose: Modify your  program from Exercise 6-2  so that each person  can have
# more than one favorite number.  Then print each person's name along with their
# favorite numbers.

# Reference: page 112 (paper) / 150 (ebook)

favorite_numbers = {
    'john': [12, 21],
    'paul': [34, 43],
    'george': [56, 65],
    'ringo': [78, 87],
    'vincent': [90],
}

for name, numbers in favorite_numbers.items():
    print()
    if len(numbers) == 1:
        print(f"{name.title()}'s favorite number is {numbers[0]}.")
    else:
        print(f"{name.title()}'s favorite number are:")
        for number in numbers:
            print('\t' + f'{number}')
#     John's favorite number are:
#             12
#             21
#
#     Paul's favorite number are:
#             34
#             43
#
#     George's favorite number are:
#             56
#             65
#
#     Ringo's favorite number are:
#             78
#             87
#
#     Vincent's favorite number is 90.
