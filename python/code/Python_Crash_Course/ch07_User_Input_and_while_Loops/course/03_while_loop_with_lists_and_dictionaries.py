# Purpose: examine practical example when a `while` loop is useful
# Reference: page 124 (paper) / 162 (ebook)

# A `while` loop is handy to progressively move items from one list into another. {{{1

# Start with users that need to be verified, and an empty list to hold confirmed
# users.   Our goal  is to  verify each  unconfirmed user,  then move  them into
# `confirmed_users`.
unconfirmed_users = ['alice', 'brian', 'candace']
confirmed_users = []

# Verify each user until there are no more unconfirmed users.
# Move each verified user into the list of confirmed users.
while unconfirmed_users:
# ---------------------^
# The  loop will  keep running  as  long as  there  are still  items inside  the
# `unconfirmed_users` list.  Once we've removed all the items (via `pop()`), the
# loop will end.  Remember that a list/tuple/dictionary can be used as a logical
# expression, which is `True` iff it's not empty.
    current_user = unconfirmed_users.pop()

    # this `print()` simulates a user being confirmed
    print(f'Verifying user: {current_user.title()}')
    # here,  we move  one item  from the  list `unconfirmed_users`  to the  list
    # `confirmed_users`
    confirmed_users.append(current_user)

# Display all confirmed users.
print('\nThe following users have been confirmed:')
for confirmed_user in confirmed_users:
    print(confirmed_user.title())
#     Verifying user: Candace
#     Verifying user: Brian
#     Verifying user: Alice
#
#     The following users have been confirmed:
#     Candace
#     Brian
#     Alice
#
# The names are printed in reverse order compared to `unconfirmed_users`.
# That's because  we've used the  `pop()` method to  extract each user  from the
# list; and without any numerical argument,  `pop()` extracts the last item (not
# the first one).  IOW, we've processed the  list from its end, rather than from
# its start.

# A `while` loop is handy to remove all instances of a specific value from a list. {{{1
# To remove an item from a list, we would use the `remove()` method.
# But that will only remove the first instance of a given value.
# To remove *all* instances, we need a `while` loop.

# The `pets` list contains the value 'cat' multiple times.
# Let's remove all of them.
pets = ['dog', 'cat', 'dog', 'goldfish', 'cat', 'rabbit', 'cat']
print(pets)

while 'cat' in pets:
#     ^-----------^
#
# So far, it's only inside `if`  statements that we've seen a logical expression
# using the membership operator `in`.  Here, we  can see that we can also use it
# in a  `while` statement.  Which  makes sense; both  `if` and `while`  expect a
# logical expression and `'value' in list` is one.
#
# This loop will end as soon as the value 'cat' can no longer be found in `pets`.
    pets.remove('cat')

print(pets)
#     ['dog', 'cat', 'dog', 'goldfish', 'cat', 'rabbit', 'cat']
#     ['dog', 'dog', 'goldfish', 'rabbit']

# A dictionary is handy to map some data to another. {{{1

# Let's build a  list of dictionaries mapping names of  people to mountains they
# would like to climb.   In the process, we'll see that in  a `while` loop we're
# not limited to a single call to `input()`;  we can call it as many times as we
# need to gather information.
responses = {}

# Set a flag to indicate that polling is active.
polling_active = True

while polling_active:
    # Prompt for the person's name and response.
    name = input('\nWhat is your name? ')
    response = input('Which mountain would you like to climb someday? ')

    # Store the response in the dictionary.
    # In effect, the `responses` dictionary maps a name to a response.
    responses[name] = response

    # Find out if anyone else is going to take the poll.
    repeat = input('Would you like to let another person respond? (yes/ no) ')
    if repeat == 'no':
        polling_active = False

# Polling is complete.  Show the results.
print('\n--- Poll results ---')
for name, response in responses.items():
    print(f'{name} would like to climb {response}.')
#     What is your name? Eric
#     Which mountain would you like to climb someday? Denali
#     Would you like to let another person respond? (yes/ no) yes
#
#     What is your name? Lynn
#     Which mountain would you like to climb someday? Devil's Thumb
#     Would you like to let another person respond? (yes/ no) no
#
#     --- Poll results ---
#     Eric would like to climb Denali.
#     Lynn would like to climb Devil's Thumb.
