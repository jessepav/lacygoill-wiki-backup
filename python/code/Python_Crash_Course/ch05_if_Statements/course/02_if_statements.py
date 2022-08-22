# Purpose: write various `if` statements
# Reference: page 78 (paper) / 116 (ebook)

age = 19

# An `if` statement executes the next statement iff its logical expression evaluates to `True`. {{{1

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

# An `if` block can contain several `elif` clauses. {{{1

age = 12

if age < 4:
    price = 0
elif age < 18:
    price = 25
# here is a second `elif` clause inside the same `if` block
elif age < 65:
    price = 40
else:
    price = 20

print(f'Your admission cost is ${price}')
#     Your admission cost is $25

# An `else` clause can be omitted even after an `elif` clause. {{{1

age = 12

if age < 4:
    price = 0
elif age < 18:
    price = 25
elif age < 65:
    price = 40
elif age >= 65:
    price = 20
# no `else` clause

print(f'Your admission cost is ${price}')
#     Your admission cost is $25

# A list/tuple/dictionary can be used as a logical expression which evaluates to `True` iff it's not empty. {{{1

requested_toppings = []

if requested_toppings:
    for requested_topping in requested_toppings:
        print(f'Adding {requested_topping}.')
    print(f'\nFinished making your pizza!')
else:
    print('Are you sure you want a plain pizza?')
#     Are you sure you want a plain pizza?
#
# Since the list is empty, execution skips  the `for` loop and jumps to the last
# `print()`.


# To test whether a list is empty, you would add the `not` operator:
#
#     if not list:
#        ^^^
