# Purpose: Turn your `if-else` chain from Exercise 5-4 into an `if-elif-else` chain.
#
#    - If the alien is green, print a message that the player earned 5 points.
#    - If the alien is yellow, print a message that the player earned 10 points.
#    - If the alien is red, print a message that the player earned 15 points.
#
#    - Write three versions of this program, making sure each message is
#      printed for the appropriate color alien.
#
# Reference: page 85 (paper) / 123 (ebook)

for alien_color in ('green', 'yellow', 'red'):
    if alien_color == 'green':
        print('you earned 5 points')
    elif alien_color == 'yellow':
        print('you earned 10 points')
    elif alien_color == 'red':
        print('you earned 15 points')
#     you earned 5 points
#     you earned 10 points
#     you earned 15 points
