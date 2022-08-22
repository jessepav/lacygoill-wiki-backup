# Purpose: Choose a color for an alien as  you did in Exercise 5-3, and write an
# `if-else` chain.
#
#    - If the alien's color is green, print a statement that the player just
#      earned 5 points for shooting the alien.
#
#    - If the alien's color isn't green, print a statement that the player just
#      earned 10 points.
#
#    - Write one version of this program that runs the `if` block and another
#      that runs the `else` block.

# Reference: page 84 (paper) / 122 (ebook)

for alien_color in ('green', 'red'):
    if alien_color == 'green':
        print('you earned 5 points')
    else:
        print('you earned 10 points')
#     you earned 5 points
#     you earned 10 points
