# Purpose: write various logical expressions
# Reference: page 72 (paper) / 110 (ebook)

# The equality operator `==` can test whether 2 string expressions are the same.{{{1

#   assignment operator
#   v
car = 'bmw'
#         equality operator
#         vv
print(car == 'bmw')
#     True

# Here,  the  expression  `car == 'bwm'`   evaluates  to  `True`  because  `car`
# evaluates to  'bmw' (assigned  in the previous  statement), which  matches the
# string on the RHS of the `==` operator.

car = 'audi'
print(car == 'bwm')
#     False
#
# This time, it evaluates to `False` because `car` evaluates to 'audi', which no
# longer matches the string on the RHS of the `==` operator.

#   To ignore the case in a string comparison, use the `lower()` method. {{{1

car = 'Audi'
print(car == 'audi')
print(car.lower() == 'audi')
#     False
#     True
#
# It's  safe to  use `lower()`  here, because  it doesn't  operate in-place;  it
# leaves the original value of the variable unchanged.
#}}}1

# For an *in*equality test, use the `!=` operator.{{{1

requested_topping = 'mushrooms'
print(requested_topping != 'anchovies')
#     True
#
# The LHS of `!=` is `requested_topping` which evaluates to 'mushrooms'.
# It's different than the RHS 'anchovies'; thus the overall expression evaluates
# to `True`.

# `==` and `!=` can be used to compare integers too.{{{1

age = 18
print(age == 18)
#     True

answer = 17
if answer != 42:
    print('That is not the correct answer.  Please try again!')
#     That is not the correct answer.  Please try again!
#}}}1

# The relational operators `<`, `<=`, `>`, `>=` can be used to compare integers.{{{1

age = 19

print(age < 21)
print(age <= 21)
print(age > 21)
print(age >= 21)
#     True
#     True
#     False
#     False

# The logical operator `and` tests whether *both* of its 2 operands evaluate to `True`.{{{1

age_0 = 22
age_1 = 18
#                 vvv
print(age_0 >= 21 and age_1 >= 21)
#     False

age_1 = 22
print(age_0 >= 21 and age_1 >= 21)
#     True

# `and` has a lower precedence than the relational operators.
# If you wrote the implicit  grouping parentheses, the previous expression would
# look like this:
#
#     print((age_0 >= 21) and (age_1 >= 21))
#           ^           ^     ^           ^

# The logical operator `or` tests whether *at least one* of its 2 operands evaluate to `True`.{{{1

age_0 = 22
age_1 = 18
print(age_0 >= 21 or age_1 >= 21)
#     True

age_0 = 18
print(age_0 >= 21 or age_1 >= 21)
#     False
#}}}1

# The membership operator `in` tests whether a value is *present* inside a list.{{{1

requested_toppings = ['mushrooms', 'onions', 'pineapple']
#                 vv
print('mushrooms' in requested_toppings)
print('pepperoni' in requested_toppings)
#     True
#     False
#
# The membership operator `not in` tests whether a value is *absent* from a list.{{{1

banned_users = ['andrew', 'carolina', 'david']
user = 'marie'
#          v----v
print(user not in banned_users)
#     True
#}}}1
