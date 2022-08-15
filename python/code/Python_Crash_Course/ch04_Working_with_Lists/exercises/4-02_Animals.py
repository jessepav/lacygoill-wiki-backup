# Purpose: Think of at least three different animals that have a common characteristic.
# Store the names of these animals in a list, and then use a `for` loop to print
# out the name of each animal.
#
#    - Modify your program to print a statement about each animal, such as:
#      "A dog would make a great pet."
#
#    - Add a line at the end of your program stating what these animals have in
#      common.  You could print a sentence such as "Any of these animals would
#      make a great pet!"

# Reference: page 56 (paper) / 94 (ebook)

animals = ['cat', 'dog', 'mouse']
for animal in animals:
    print(animal)
    #     cat
    #     dog
    #     mouse

print()

for animal in animals:
    print(f'A {animal} would make a great pet.')
print('Any of these animals would make a great pet!')
#     A cat would make a great pet.
#     A dog would make a great pet.
#     A mouse would make a great pet.
#     Any of these animals would make a great pet!
