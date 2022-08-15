# Purpose: write various `if` statements
# Reference: page 78 (paper) / 116 (ebook)

# An `if` statement executes the next statement iff its logical expression evaluates to `True`. {{{1

age = 19
if age >= 18:
    print('You are old enough to vote!')
#     You are old enough to vote!
#
# Here, the logical expression is `age >= 18`.
# It evaluates to `True` because `age` evaluates to 19 which is greater than 18.
# Because the logical expression is `True`, the next `print()` is executed.

# The body of an `if` block is not limited to 1 statement. {{{1

if age >= 18:
    print('You are old enough to vote!')
    # This line is part of the `if` block because it's also indented.
    print('Have you registered to vote yet?')
#     You are old enough to vote!
#     Have you registered to vote yet?

# An `else` clause lets you run different statements when the logical expression is `False`. {{{1

age = 17
if age >= 18:
    print('You are old enough to vote!')
    print('Have you registered to vote yet?')
# this `else` clause will only be run if `age >= 18` is `False`
else:
    print('Sorry, you are too young to vote.')
    print('Please register to vote as soon as you turn 18!')
#     Sorry, you are too young to vote.
#     Please register to vote as soon as you turn 18!
#
# This time, we get different messages; the ones specified in the `else` clause.
# That's because we've lowered the value in the variable `age` which changes the
# evaluation of `age >= 18`.

# An `elif` clause lets you run different statements when the `if` test fails, but another test passes. {{{1

age = 12
if age < 4:
    price = 0
elif age < 18:
    price = 25
else:
    price = 40
print(f'Your admission cost is ${price}')
#     Your admission cost is $25
#
# Notice that Python only runs the `elif` clause; not the subsequent `else`.
# If `else` had been run, the final message would have reported the price `$40`;
# not `$25`.
#
# That's because only 1 clause can be run inside an `if` block.
# As soon  as a  test passes,  and the  corresponding clause  has been  run, the
# execution jumps out of the whole `if` block.
