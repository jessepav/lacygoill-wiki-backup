# Purpose: Write a program that polls users about their dream vacation.  Write a
# prompt similar to "If you could visit  one place in the world, where would you
# go?".  Include a block of code that prints the results of the poll.

# Reference: page 127 (paper) / 165 (ebook)

places = {}

polling_active = True
while polling_active:
    name = input('\nWhat is your name? ')
    place = input('If you could visit one place in the world, where would you go? ')
    places[name] = place
    repeat = input('Would you like to let another person respond? (yes/ no) ')
    if repeat == 'no':
        polling_active = False

print('\n--- Poll results ---')
for name, place in places.items():
    print(f'{name} would like to visit {place}.')
#     What is your name? Eric
#     If you could visit one place in the world, where would you go? Berlin
#     Would you like to let another person respond? (yes/ no) yes
#
#     What is your name? Lynn
#     If you could visit one place in the world, where would you go? London
#     Would you like to let another person respond? (yes/ no) no
#
#     --- Poll results ---
#     Eric would like to visit Berlin.
#     Lynn would like to visit London.
