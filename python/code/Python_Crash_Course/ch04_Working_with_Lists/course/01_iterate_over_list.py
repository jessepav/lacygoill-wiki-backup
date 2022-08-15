# Purpose: iterate over items in list
# Reference: page 50 (paper) / 88 (ebook)

magicians = ['alice', 'david', 'carolina']

# simple `for` loop {{{1

# This line causes Python to iterate over the items inside the `magicians` list.
# In each  iteration, the  item which pulled  from the list  is assigned  to the
# `magician` variable.
for magician in magicians:
    print(magician)
#     alice
#     david
#     carolina

# more complex `for` loop {{{1

# The variable used to store the item (here `magician`) is not special.
# That is, you can do with it whatever is allowed for a regular variable.
for magician in magicians:
    print(f'{magician.title()}, that was a great trick!')
#     Alice, that was a great trick!
#     David, that was a great trick!
#     Carolina, that was a great trick!

# `for` loop with several statements {{{1

# A `for` loop can repeat as many statements as you want.
# But for your statements to remain inside a loop, they must all be indented.
for magician in magicians:
    print(f'{magician.title()}, that was a great trick!')
    #       insert an empty line between 2 consecutive set of messages
    #                                                               vv
    print(f"I can't wait to see your next trick, {magician.title()}.\n")
#     Alice, that was a great trick!
#     I can't wait to see your next trick, Alice.
#
#     David, that was a great trick!
#     I can't wait to see your next trick, David.
#
#     Carolina, that was a great trick!
#     I can't wait to see your next trick, Carolina.

# `for` loop followed by another statement {{{1

# To run a statement after a loop, decrease its indentation level.
for magician in magicians:
    print(f'{magician.title()}, that was a great trick!')
    print(f"I can't wait to see your next trick, {magician.title()}.\n")

# This statement will  be run *after* exiting the loop,  because its indentation
# is lower than the statements inside the loop's body.
print('Thank you, everyone.  That was a great magic show!')
#     Alice, that was a great trick!
#     I can't wait to see your next trick, Alice.
#
#     David, that was a great trick!
#     I can't wait to see your next trick, David.
#
#     Carolina, that was a great trick!
#     I can't wait to see your next trick, Carolina.
#
#     Thank you, everyone.  That was a great magic show!
