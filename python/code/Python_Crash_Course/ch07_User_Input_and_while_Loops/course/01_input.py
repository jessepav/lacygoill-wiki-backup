# Purpose: ask for user input
# Reference: page 114 (paper) / 152 (ebook)

# `input()` lets you ask the user for some info, and save it in a variable {{{1

#                                       prompt
#               v-----------------------------------------------------v
message = input('Tell me something, and I will repeat it back to you: ')
print(message)
#     Tell me something, and I will repeat it back to you: Hello everyone!
#     Hello everyone!
#
# Whatever the user has written when pressing Enter to validate their input will
# be saved  in the  variable `message`.  You  can then use  the latter  like any
# other variable.

#   The prompt should explain clearly to the user what information your program needs to get. {{{1

# always append a space to the prompt, so that it's well-separated from the input
#                                     v
name = input('Pleaser enter your name: ')
print(f'\nHello, {name}!')
#     Pleaser enter your name: Eric
#
#     Hello, Eric!

#   The prompt can span over multiple lines. {{{1

# For the strings to be concatenated, you could also replace the parens with the `+=` assignment operator.{{{
#
#     prompt = 'If you tell us who you are, we can personalize the messages you see.'
#     prompt += '\nWhat is your first name? '
#            ^^
#
# The latter does not completely *overwrite*  the existing value of the variable
# on the LHS.  Instead,  it *appends* the value on the RHS  to the current value
# held by the variable.
#}}}
prompt = (
    'If you tell us who you are, we can personalize the messages you see.'
    '\nWhat is your first name? '
)

name = input(prompt)
print(f'\nHello, {name}!')
#     If you tell us who you are, we can personalize the messages you see.
#     What is your first name? Eric
#
#     Hello, Eric!
#}}}1

# `input()` always returns a string.  Even if the user has input a number. {{{1

age = input('How old are you? ')
print(type(age))
#     How old are you? 21
#     <class 'str'>
#             ^^^

#   But you might need to do some arithmetic with an input number.  If so, use `int()` to coerce it. {{{1

height = int(input('How tall are you, in inches? '))
#        ^^^
#
# Without `int()`, the next arithmetic comparison `>=` would fail:
#
#     TypeError: '>=' not supported between instances of 'str' and 'int'

if height >= 48:
    print("\nYou're tall enough to ride!")
else:
    print("\nYou'll be able to ride when you're a little older.")
#     How tall are you, in inches? 71
#
#     You're tall enough to ride!

#   To test whether an input number is even or odd, use the modulo operator `%`. {{{1

number = int(input("Enter a number, and I'll tell you if it's even or odd: "))

# An integer is even iff its remainder in a division by 2 is 0.
#         v
if number % 2 == 0:
    print(f'\nThe number {number} is even.')
else:
    print(f'\nThe number {number} is odd.')
#     Enter a number, and I'll tell you if it's even or odd: 42
#
#     The number 42 is even.
