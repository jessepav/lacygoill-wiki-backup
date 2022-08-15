# Purpose: Using one  of the  programs you  wrote in  this chapter,  add several
# lines to the end of the program that do the following:
#
#    - Print the message "The first three items in the list are:".  Then use
#      a slice to print the first three items from that program's list.
#
#    - Print the message "Three items from the middle of the list are:".  Use
#      a slice to print three items from the middle of the list.
#
#    - Print the message "The last three items in the list are:".  Use a slice
#      to print the last three items in the list.

# Reference: page 65 (paper) / 103 (ebook)

planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

print('The first three items in the list are:')
for planet in planets[:3]:
    print(planet)
#     The first three items in the list are:
#     Mercury
#     Venus
#     Earth

print('\nThree items from the middle of the list are:')
for planet in planets[2:5]:
    print(planet)
#     Three items from the middle of the list are:
#     Earth
#     Mars
#     Jupiter

print('\nThe last three items in the list are:')
for planet in planets[-3:]:
    print(planet)
#     The last three items in the list are:
#     Saturn
#     Uranus
#     Neptune
